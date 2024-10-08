# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

#
# Hooks specific to the HPC2N GPU microbenchmark tests.
#


def set_gpu_arch(self):
    '''Set the compile options for the gpu microbenchmarks.'''

    cs = self.current_system.name
    cp = self.current_partition.fullname
    cn = self.current_partition.name
    self.gpu_arch = None

    # Nvidia options
    self.gpu_build = 'cuda'
    if cs in {'alvis', 'kebnekaise'}:
        if 'K80' in cn:
            self.gpu_arch = '37'
        if 'V100' in cn:
            self.gpu_arch = '70'
        if 'T4' in cn:
            self.gpu_arch = '75'
        if 'A40' in cn:
            self.gpu_arch = '86'
        if 'A6000' in cn:
            self.gpu_arch = '86'
        if 'A100' in cn:
            self.gpu_arch = '80'
        if 'l40' in cn:
            self.gpu_arch = '89'
        if 'h100' in cn:
            self.gpu_arch = '90'
    elif cs in {'UmU-Cloud'}:
        self.gpu_arch = '80'
    elif cs in {'dom', 'daint'}:
        self.gpu_arch = '60'
        if self.current_environ.name not in {'PrgEnv-nvidia'}:
            self.modules = ['craype-accel-nvidia60', 'cdt-cuda']
        else:
            self.modules = ['cdt-cuda/21.05']

    elif cs in {'arola', 'tsa'}:
        self.gpu_arch = '70'
        self.modules = ['cuda/10.1.243']
    elif cs in {'ault'}:
        self.modules = ['cuda']
        if cp in {'ault:amdv100', 'ault:intelv100'}:
            self.gpu_arch = '70'
        elif cp in {'ault:amda100'}:
            self.gpu_arch = '80'

    # AMD options
    if cp in {'ault:amdvega'}:
        self.gpu_build = 'hip'
        self.modules = ['rocm']
        self.gpu_arch = 'gfx900,gfx906'


def set_num_gpus_per_node(self):
    '''Set the GPUs per node for the GPU microbenchmarks.'''

    cs = self.current_system.name
    cp = self.current_partition.fullname
    cn = self.current_partition.name

    if cs in {'alvis', 'kebnekaise'}:
        if cn in {'1xK80', '2xV100', '2xA6000', '2xV100', '2xA100', '2xMI100'}:
            self.num_gpus_per_node = 2
        elif cn in {'2xK80', '4xV100', '4xA100_MEM256', '4xA100_MEM512', '4xA100fat', '4xA40'}:
            self.num_gpus_per_node = 4
        elif cn in {'4xK80', '8xT4'}:
            self.num_gpus_per_node = 8

    if self.num_gpus_per_node is None:
        gpu_devices = self.current_partition.select_devices('gpu')
        if gpu_devices:
            self.num_gpus_per_node = gpu_devices[0].num_devices
        else:
            self.num_gpus_per_node = 1
