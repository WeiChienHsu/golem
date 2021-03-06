from os import path

from golem.environments.minperformancemultiplier import MinPerformanceMultiplier
from golem.testutils import DatabaseFixture

from golem.environments.environment import Environment
from golem.model import Performance
from golem.testutils import PEP8MixIn


class EnvTest(DatabaseFixture, PEP8MixIn):
    PEP8_FILES = ["golem/environments/environment.py"]

    def setUp(self):
        super().setUp()
        self.env = Environment()

    def test_get_performance(self):
        perf_value = 6666.6
        perf = Performance(environment_id="DEFAULT", value=perf_value)
        perf.save()
        result = self.env.get_performance()
        self.assertTrue(result == perf_value)

    def test_get_source_code(self):
        assert self.env.get_source_code() is None

        file_name = path.join(self.path, "mainprogramfile")
        self.env.main_program_file = file_name
        assert self.env.get_source_code() is None

        with open(file_name, 'w') as f:
            f.write("PROGRAM CODE")

        self.env.main_program_file = file_name
        assert self.env.get_source_code() == "PROGRAM CODE"

    def test_check_software(self):
        assert not self.env.check_software()
        self.env.allow_custom_main_program_file = True
        assert self.env.check_software()
        self.env.allow_custom_main_program_file = False

        file_name = path.join(self.path, "mainprogramfile")
        self.env.main_program_file = file_name

        with open(file_name, 'w') as f:
            f.write("PROGRAM CODE")

        assert self.env.check_software()

    def test_run_default_benchmark(self):
        assert Environment.get_performance() == 0.0
        assert Environment.run_default_benchmark(save=True) > 0.0
        assert Environment.get_performance() > 0.0

    def test_get_min_accepted_performance_default(self):
        self.assertEqual(MinPerformanceMultiplier.get(), 0.0)
        self.assertEqual(self.env.get_min_accepted_performance(), 0.0)

    def test_get_min_accepted_performance(self):
        p = Performance(environment_id=Environment.get_id(),
                        min_accepted_step=100)
        p.save()
        MinPerformanceMultiplier.set(3.141)
        self.assertEqual(MinPerformanceMultiplier.get(), 3.141)
        self.assertEqual(self.env.get_min_accepted_performance(), 314.1)
