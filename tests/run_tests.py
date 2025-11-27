#!/usr/bin/env python3
"""
Test Runner
Comprehensive test runner for all test suites
"""

import os
import sys
import django
import unittest
import time
import argparse
from io import StringIO

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'A2SL.settings')
django.setup()

def run_test_suite(test_suite_name, test_class=None, verbose=False):
    """Run a specific test suite"""
    print(f"\n{'='*60}")
    print(f"Running {test_suite_name} Tests")
    print(f"{'='*60}")
    
    # Import test modules
    if test_suite_name == "unit":
        from tests.test_nlp_unit import TestNLPUnit
        test_class = TestNLPUnit
    elif test_suite_name == "integration":
        from tests.test_integration import TestIntegration
        test_class = TestIntegration
    elif test_suite_name == "functional":
        from tests.test_functional import TestFunctional
        test_class = TestFunctional
    elif test_suite_name == "regression":
        from tests.test_regression import TestRegression
        test_class = TestRegression
    elif test_suite_name == "config":
        from tests.test_config import TestConfig, TestEnvironment, TestUtilities
        test_class = TestConfig
    elif test_suite_name == "all":
        return run_all_tests(verbose)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2 if verbose else 1)
    result = runner.run(suite)
    
    return result

def run_all_tests(verbose=False):
    """Run all test suites"""
    print(f"\n{'='*60}")
    print("Running ALL Test Suites")
    print(f"{'='*60}")
    
    # Import all test modules
    from tests.test_nlp_unit import TestNLPUnit
    from tests.test_integration import TestIntegration
    from tests.test_functional import TestFunctional
    from tests.test_regression import TestRegression
    from tests.test_config import TestConfig, TestEnvironment, TestUtilities
    
    # Create comprehensive test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestNLPUnit,
        TestIntegration,
        TestFunctional,
        TestRegression,
        TestConfig,
        TestEnvironment,
        TestUtilities
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run all tests
    runner = unittest.TextTestRunner(verbosity=2 if verbose else 1)
    result = runner.run(suite)
    
    return result

def generate_test_report(result):
    """Generate a test report"""
    print(f"\n{'='*60}")
    print("TEST REPORT")
    print(f"{'='*60}")
    
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    skipped = len(result.skipped) if hasattr(result, 'skipped') else 0
    passed = total_tests - failures - errors - skipped
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed}")
    print(f"Failed: {failures}")
    print(f"Errors: {errors}")
    print(f"Skipped: {skipped}")
    print(f"Success Rate: {(passed/total_tests)*100:.1f}%")
    
    if failures > 0:
        print(f"\n{'='*60}")
        print("FAILURES")
        print(f"{'='*60}")
        for test, traceback in result.failures:
            print(f"FAIL: {test}")
            print(traceback)
            print("-" * 40)
    
    if errors > 0:
        print(f"\n{'='*60}")
        print("ERRORS")
        print(f"{'='*60}")
        for test, traceback in result.errors:
            print(f"ERROR: {test}")
            print(traceback)
            print("-" * 40)
    
    return {
        'total': total_tests,
        'passed': passed,
        'failed': failures,
        'errors': errors,
        'skipped': skipped,
        'success_rate': (passed/total_tests)*100
    }

def main():
    """Main test runner function"""
    parser = argparse.ArgumentParser(description='Run tests for Sanket Bhasha')
    parser.add_argument('--suite', choices=['unit', 'integration', 'functional', 'regression', 'config', 'all'], 
                       default='all', help='Test suite to run')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--report', action='store_true', help='Generate detailed report')
    
    args = parser.parse_args()
    
    print("🧪 Sanket Bhasha Test Suite")
    print("=" * 60)
    print(f"Test Suite: {args.suite}")
    print(f"Verbose: {args.verbose}")
    print(f"Report: {args.report}")
    
    start_time = time.time()
    
    try:
        # Run tests
        result = run_test_suite(args.suite, verbose=args.verbose)
        
        # Generate report
        if args.report:
            report = generate_test_report(result)
            
            # Save report to file
            with open('test_report.txt', 'w') as f:
                f.write(f"Test Report - {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 60 + "\n")
                f.write(f"Total Tests: {report['total']}\n")
                f.write(f"Passed: {report['passed']}\n")
                f.write(f"Failed: {report['failed']}\n")
                f.write(f"Errors: {report['errors']}\n")
                f.write(f"Skipped: {report['skipped']}\n")
                f.write(f"Success Rate: {report['success_rate']:.1f}%\n")
            
            print(f"\n📊 Report saved to: test_report.txt")
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n⏱️  Total execution time: {duration:.2f} seconds")
        
        # Exit with appropriate code
        if result.failures or result.errors:
            print(f"\n❌ Tests completed with failures/errors")
            sys.exit(1)
        else:
            print(f"\n✅ All tests passed successfully!")
            sys.exit(0)
            
    except Exception as e:
        print(f"\n💥 Test runner failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
