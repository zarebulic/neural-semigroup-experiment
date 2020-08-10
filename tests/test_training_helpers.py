"""
   Copyright 2019-2020 Boris Shminke

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
# pylint: disable-all
import sys
from unittest import TestCase
from unittest.mock import patch

import torch
from ignite.engine import Engine, Events
from ignite.handlers import EarlyStopping, ModelCheckpoint
from torch.nn import Module

from neural_semigroups.magma import Magma
from neural_semigroups.training_helpers import (
    add_early_stopping_and_checkpoint,
    associative_ratio,
    get_arguments,
    get_loaders,
    load_database_as_cubes,
)
from neural_semigroups.utils import FOUR_GROUP


class TestTrainingHelpers(TestCase):
    def setUp(self):
        torch.manual_seed(47)

    def test_get_arguments(self):
        args = "prog --cardinality 2 --train_size 1 --validation_size 1"
        with patch.object(sys, "argv", args.split(" ")):
            get_arguments()

    @patch("neural_semigroups.training_helpers.load_database_as_cubes")
    def test_get_loaders(self, load_database_as_cubes_mock):
        train = torch.tensor([1])
        train_labels = torch.tensor([2])
        validation = torch.tensor([3])
        validation_labels = torch.tensor([4])
        test = torch.tensor([5])
        test_labels = torch.tensor([6])
        load_database_as_cubes_mock.return_value = (
            train,
            validation,
            test,
            train_labels,
            validation_labels,
            test_labels,
        )
        train_loader, validation_loader, test_loader = get_loaders(
            "filename", 1, 1, 1, 0.0
        )
        batch = [i for i in train_loader][0]
        self.assertIsInstance(batch, list)
        self.assertEqual(len(batch), 2)
        self.assertTrue(torch.allclose(batch[0], train))
        self.assertTrue(torch.allclose(batch[1], train_labels))
        batch = [i for i in validation_loader][0]
        self.assertIsInstance(batch, list)
        self.assertEqual(len(batch), 2)
        self.assertTrue(torch.allclose(batch[0], validation))
        self.assertTrue(torch.allclose(batch[1], validation_labels))
        batch = [i for i in test_loader][0]
        self.assertIsInstance(batch, list)
        self.assertEqual(len(batch), 2)
        self.assertTrue(torch.allclose(batch[0], test))
        self.assertTrue(torch.allclose(batch[1], test_labels))

    def test_load_database_as_cubes(self):
        half_result = [
            torch.tensor(
                [
                    [[[1.0, 0.0], [1.0, 0.0]], [[0.0, 1.0], [0.0, 1.0]]],
                    [[[1.0, 0.0], [0.0, 1.0]], [[1.0, 0.0], [0.0, 1.0]]],
                ]
            ),
            torch.tensor(
                [
                    [[[1.0, 0.0], [1.0, 0.0]], [[1.0, 0.0], [1.0, 0.0]]],
                    [[[0.0, 1.0], [0.0, 1.0]], [[0.0, 1.0], [0.0, 1.0]]],
                ]
            ),
            torch.tensor(
                [
                    [[[1.0, 0.0], [1.0, 0.0]], [[1.0, 0.0], [0.0, 1.0]]],
                    [[[1.0, 0.0], [0.0, 1.0]], [[0.0, 1.0], [1.0, 0.0]]],
                    [[[1.0, 0.0], [0.0, 1.0]], [[0.0, 1.0], [0.0, 1.0]]],
                    [[[0.0, 1.0], [1.0, 0.0]], [[1.0, 0.0], [0.0, 1.0]]],
                ]
            ),
        ]
        true_result = half_result + half_result
        result = load_database_as_cubes(2, 1, 1, 0.0)
        for i, tensor in enumerate(result):
            self.assertTrue(tensor.allclose(true_result[i]))

    def test_associate_ratio(self):
        ratio = associative_ratio(
            Magma(FOUR_GROUP).probabilistic_cube.view(-1, 4, 4, 4),
            torch.tensor(0.0),
        )
        self.assertTrue(torch.tensor(1.0).allclose(ratio))

    def test_add_early_stopping_and_checkpoint(self):
        module = Module()
        evaluator = Engine(lambda x, y: 0.0)
        trainer = Engine(lambda x, y: 0.0)
        add_early_stopping_and_checkpoint(evaluator, trainer, "test", module)
        completed_handlers = evaluator._event_handlers[Events.COMPLETED]
        self.assertEqual(len(completed_handlers), 2)
        self.assertIsInstance(completed_handlers[0][0], EarlyStopping)
        self.assertIsInstance(completed_handlers[1][0], ModelCheckpoint)
