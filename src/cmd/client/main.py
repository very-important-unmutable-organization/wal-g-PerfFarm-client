import logging
import time
from typing import Dict, List

import yaml

from internal.base.base_wrapper import BaseWrapper
from internal.base.benchmark_runner import BenchmarkRunner
from internal.benchmarks.run_wal_fetch_n_times import RunWalFetchNTimes
from internal.wrappers.random_wal_generator import RandomWalGenerator
from utils.const import CONFIGURATION_WRAPPERS_KEY, CONFIGURATION_CLASS_KEY, CONFIGURATION_KWARGS_KEY, \
    CONFIGURATION_BENCHMARKS_KEY, CONFIGURATION_WRAPPER_KEY, CONFIGURATION_BENCH_NAME_KEY
from utils.generate_walg_config import generate_walg_config

logging.basicConfig(
    format='[%(levelname)s] [%(asctime)s]  %(message)s',
    level=logging.DEBUG,
    datefmt='%Y/%m/%d %H:%M:%S',
)

WRAPPER_CLASSES = {
    'RandomWalGenerator': RandomWalGenerator,
}

BENCHMARK_CLASSES = {
    'RunWalFetchNTimes': RunWalFetchNTimes,
}


def read_wrappers(configuration: Dict) -> Dict[str, BaseWrapper]:
    wrappers = {}  # Dict from name to wrapper
    for name, wrapper_dict in configuration[CONFIGURATION_WRAPPERS_KEY].items():
        if CONFIGURATION_CLASS_KEY not in wrapper_dict:
            raise ValueError(f'{CONFIGURATION_CLASS_KEY} is required field in wrapper description')

        class_name = wrapper_dict[CONFIGURATION_CLASS_KEY]
        if class_name not in WRAPPER_CLASSES:
            raise ValueError(f'{class_name} wrapper is not implemented yet')

        klass = WRAPPER_CLASSES[class_name]
        kwargs = wrapper_dict.get(CONFIGURATION_KWARGS_KEY, {})

        wrappers[name] = klass(**kwargs)

    return wrappers


def read_benchmarks(configuration, wrappers_lookup) -> List[BenchmarkRunner]:
    benchmark_runners = []
    for bench_dict in configuration[CONFIGURATION_BENCHMARKS_KEY]:
        if CONFIGURATION_CLASS_KEY not in bench_dict:
            raise ValueError(f'{CONFIGURATION_CLASS_KEY} is required field in benchmark description')

        class_name = bench_dict['class']
        if class_name not in BENCHMARK_CLASSES:
            raise ValueError(f'{class_name} benchmark is not implemented yet')

        if CONFIGURATION_BENCH_NAME_KEY not in bench_dict:
            raise ValueError(f'{CONFIGURATION_BENCH_NAME_KEY} is required field in benchmark description')

        name = bench_dict[CONFIGURATION_BENCH_NAME_KEY]
        klass = BENCHMARK_CLASSES[class_name]
        kwargs = bench_dict.get(CONFIGURATION_KWARGS_KEY, {})
        wrappers = []

        for wrapper in bench_dict[CONFIGURATION_WRAPPERS_KEY]:
            wrapper_name = wrapper[CONFIGURATION_WRAPPER_KEY]
            if wrapper_name not in wrappers_lookup:
                raise ValueError(f'unknown wrapper {wrapper_name} in benchmark {name}')

            wrappers.append(wrappers_lookup[wrapper_name])

        bench = klass(**kwargs)
        benchmark_runners.append(BenchmarkRunner(name, bench, wrappers))

    return benchmark_runners


def main():
    generate_walg_config()
    configuration = {}
    with open('/opt/bench.yaml', 'r') as f:
        configuration = yaml.safe_load(f)

    wrappers = read_wrappers(configuration)
    benchmarks = read_benchmarks(configuration, wrappers)

    results = []
    logging.info('running of benchmarks started')
    for runner in benchmarks:
        runner_results = runner.run()
        results.extend(runner_results)

    logging.info('all benchmarks has been run!')

    logging.info('\n'.join(str(res) for res in results))


if __name__ == '__main__':
    main()
    time.sleep(999999)