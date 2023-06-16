import getpass
import os

import reframe as rfm
import reframe.utility.sanity as sn


class MdtestCheck(rfm.RunOnlyRegressionTest):
    base_dir = parameter(['/pfs/stor10/io-test',
                          '/cephyr/NOBACKUP/priv/c3-alvis/reframe/io-test',
                          '/cephyr2/NOBACKUP/priv/c3-alvis/reframe/io-test',
                          '/mimer/NOBACKUP/groups/c3-staff/reframe/io-test',
                          ])
    username = getpass.getuser()
    time_limit = '15m'
    maintainers = ['ÅS']
    tags = {'ops'}

    @run_after('init')
    def set_description(self):
        self.descr = f'MDtest check ({self.base_dir})'

    @run_after('init')
    def add_fs_tags(self):
        self.tags |= {self.base_dir}

    @run_after('init')
    def set_fs_information(self):
        self.fs = {
            '/pfs/stor10/io-test': {
                'valid_systems': ['kebnekaise'],
                'kebnekaise': {
                    'num_tasks': 28,
                    'num_tasks_per_node': 28,
                },
                'reference': {
                    'create': (0, -0.1, None, 'files/s'),
                    'stat': (0, -0.1, None, 'files/s'),
                    'read': (0, -0.1, None, 'files/s'),
                    'remove': (0, -0.1, None, 'files/s'),
                    'tree_create': (0, -0.1, None, 'dirs/s'),
                    'tree_remove': (0, -0.1, None, 'dirs/s'),
                },
            },
            '/cephyr/NOBACKUP/priv/c3-alvis/reframe/io-test': {
                'valid_systems': ['alvis'],
                'alvis:CPUonly': {
                    'num_tasks': 32,
                    'num_tasks_per_node': 32,
                },
                'alvis:4xA100_MEM256': {
                    'num_tasks': 64,
                    'num_tasks_per_node': 64,
                },
                'alvis:4xA100_MEM512': {
                    'num_tasks': 64,
                    'num_tasks_per_node': 64,
                },
                'reference': {
                    'create': (4000, -0.1, None, 'files/s'),
                    'stat': (18000, -0.1, None, 'files/s'),
                    'read': (7000, -0.1, None, 'files/s'),
                    'remove': (5400, -0.1, None, 'files/s'),
                    'tree_create': (8, -0.1, None, 'dirs/s'),
                    'tree_remove': (3, -0.1, None, 'dirs/s'),
                },
            },
            '/cephyr2/NOBACKUP/priv/c3-alvis/reframe/io-test': {
                'valid_systems': ['alvis'],
                'alvis:CPUonly': {
                    'num_tasks': 32,
                    'num_tasks_per_node': 32,
                },
                'alvis:4xA100_MEM256': {
                    'num_tasks': 64,
                    'num_tasks_per_node': 64,
                },
                'alvis:4xA100_MEM512': {
                    'num_tasks': 64,
                    'num_tasks_per_node': 64,
                },
                'reference': {
                    'create': (4000, -0.1, None, 'files/s'),
                    'stat': (18000, -0.1, None, 'files/s'),
                    'read': (7000, -0.1, None, 'files/s'),
                    'remove': (5400, -0.1, None, 'files/s'),
                    'tree_create': (8, -0.1, None, 'dirs/s'),
                    'tree_remove': (3, -0.1, None, 'dirs/s'),
                },
            },
            '/mimer/NOBACKUP/groups/c3-staff/reframe/io-test': {
                'valid_systems': ['alvis'],
                'alvis:CPUonly': {
                    'num_tasks': 32,
                    'num_tasks_per_node': 32,
                },
                'alvis:4xA100_MEM256': {
                    'num_tasks': 48,
                    'num_tasks_per_node': 48,
                },
                'alvis:4xA100_MEM512': {
                    'num_tasks': 64,
                    'num_tasks_per_node': 64,
                },
                'reference': {
                    'create': (70000, -0.1, None, 'files/s'),
                    'stat': (210000, -0.1, None, 'files/s'),
                    'read': (110000, -0.1, None, 'files/s'),
                    'remove': (105000, -0.1, None, 'files/s'),
                    'tree_create': (10, -0.1, None, 'dirs/s'),
                    'tree_remove': (1, -0.1, None, 'dirs/s'),
                },
            },
        }

        # Setting some default values
        for data in self.fs.values():
            data.setdefault('nr_dirs_files_per_proc', '1000000')
            data.setdefault('iterations', '1')
            data.setdefault('io_api', 'POSIX')
            data.setdefault('stride', '1')
            data.setdefault('hierarch_depth', '0')
            data.setdefault('stonewall_timer', '300')
            data.setdefault(
                'reference',
                {
                    'create': (0, -0.1, None, 'files/s'),
                    'stat': (0, -0.1, None, 'files/s'),
                    'read': (0, -0.1, None, 'files/s'),
                    'remove': (0, -0.1, None, 'files/s'),
                    'tree_create': (0, -0.1, None, 'dirs/s'),
                    'tree_remove': (0, -0.1, None, 'dirs/s'),
                },
            )
            data.setdefault('dummy', {})  # entry for unknown systems

    @run_after('init')
    def set_performance_reference(self):
        # Converting the references from each fs to per system.
        self.reference = {
            '*': self.fs[self.base_dir]['reference']
        }

    @run_after('init')
    def set_valid_systems(self):
        self.valid_systems = self.fs[self.base_dir]['valid_systems']

        cur_sys = self.current_system.name
        if cur_sys not in self.fs[self.base_dir]:
            cur_sys = 'dummy'

        vpe = 'valid_prog_environs'
        penv = self.fs[self.base_dir][cur_sys].get(vpe, ['builtin'])
        self.valid_prog_environs = penv


    @run_before('run')
    def set_tasks(self):
        cur_sys = self.current_system.name
        fullname = self.current_partition.fullname
        if cur_sys not in self.fs[self.base_dir]:
            cur_sys = 'dummy'
        if fullname not in self.fs[self.base_dir]:
            fullname = cur_sys

        tpn = self.fs[self.base_dir][cur_sys].get('num_tasks_per_node', 1)
        tpn = self.fs[self.base_dir][fullname].get('num_tasks_per_node', tpn)
        cpt = self.fs[self.base_dir][cur_sys].get('cpus_per_task', 1)
        cpt = self.fs[self.base_dir][fullname].get('cpus_per_task', cpt)
        nt = self.fs[self.base_dir][cur_sys].get('num_tasks', 1)
        nt = self.fs[self.base_dir][fullname].get('num_tasks', nt)
        self.num_tasks = nt
        self.tpn = tpn
        self.num_cpus_per_task = cpt

    @run_after('init')
    def set_modules(self):
        module = {
            'kebnekaise': ['foss/2022a', 'IOR/3.3.0'],
            'alvis': ['IOR/3.3.0-gompi-2022a'],
        }
        self.modules = module.get(self.current_system.name)

    @run_before('run')
    def prepare_run(self):
        # Default umask is 0022, which generates file permissions -rw-r--r--
        # we want -rw-rw-r-- so we set umask to 0002
        os.umask(2)
        test_dir = os.path.join(self.base_dir, self.username, '.mdtest')
        target_dir = os.path.join(test_dir,
                                 f'.mdtest.{self.current_partition.name}')
        self.prerun_cmds = [f'mkdir -p {test_dir}']
        self.executable = 'mdtest'

        # executable options depends on the file system
        nr_files = self.fs[self.base_dir]['nr_dirs_files_per_proc']
        iterations = self.fs[self.base_dir]['iterations']
        io_api = self.fs[self.base_dir]['io_api']
        stonewall_timer = self.fs[self.base_dir]['stonewall_timer']
        stride = self.fs[self.base_dir]['stride']
        hierarch_depth = self.fs[self.base_dir]['hierarch_depth']
        self.executable_opts += ['-L', '-F', '-u ', '-Y', '-W', stonewall_timer,
                                '-a', io_api, '-n', nr_files, '-i', iterations,
                                '-N', stride, '-z', hierarch_depth,
                                '-d', target_dir]


@rfm.simple_test
class MdtestFullCheck(MdtestCheck):
    executable_opts = []
    tags = {'ops', 'maintenance'}
    tags |= {'write', 'read'}

    @sanity_function
    def assert_output(self):
        return sn.assert_found(r'^\s+File creation\s+:\s', self.stdout) and sn.assert_found(r'^\s+Tree removal\s+:\s', self.stdout)

    @run_after('init')
    def set_perf_patterns(self):
        self.perf_patterns = {
            'file_create': sn.extractsingle(
                r'^\s+File creation\s+:\s+[0-9.]+\s+[0-9.]+\s+(?P<file_create>\S+)\s+', self.stdout,
                'file_create', float),
            'file_stat': sn.extractsingle(
                r'^\s+File stat\s+:\s+[0-9.]+\s+[0-9.]+\s+(?P<file_stat>\S+)\s+', self.stdout,
                'file_stat', float),
            'file_read': sn.extractsingle(
                r'^\s+File read\s+:\s+[0-9.]+\s+[0-9.]+\s+(?P<file_read>\S+)\s+', self.stdout,
                'file_read', float),
            'file_removal': sn.extractsingle(
                r'^\s+File removal\s+:\s+[0-9.]+\s+[0-9.]+\s+(?P<file_removal>\S+)\s+', self.stdout,
                'file_removal', float),
            'tree_create': sn.extractsingle(
                r'^\s+Tree creation\s+:\s+[0-9.]+\s+[0-9.]+\s+(?P<tree_create>\S+)\s+', self.stdout,
                'tree_create', float),
            'tree_removal': sn.extractsingle(
                r'^\s+Tree removal\s+:\s+[0-9.]+\s+[0-9.]+\s+(?P<tree_removal>\S+)\s+', self.stdout,
                'tree_removal', float),
        }