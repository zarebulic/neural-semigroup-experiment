"""
   Copyright 2019-2021 Boris Shminke

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
from associator_loss import AssociatorLoss
from constant_baseline import ConstantBaseline
from cyclic_group import CyclicGroup
from denoising_autoencoder import MagmaDAE
from mace4_semigroups_dataset import Mace4Semigroups
from magma import Magma
from precise_guess_loss import PreciseGuessLoss
from semigroups_dataset import SemigroupsDataset
from smallsemi_dataset import Smallsemi
