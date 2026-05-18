#!/usr/bin/env python
"""Test script to verify CSV and Excel file format support"""

import pandas as pd
import os

def test_csv_loading():
    """Test loading CSV format"""
    csv_path = "data/Refund_Claims_Data.csv"
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            print(f"✅ CSV Format Test PASSED")
            print(f"   - File: {csv_path}")
            print(f"   - Rows: {len(df)}")
            print(f"   - Columns: {list(df.columns)}")
            return True
        except Exception as e:
            print(f"❌ CSV Format Test FAILED: {str(e)}")
            return False
    else:
        print(f"⚠️  CSV file not found: {csv_path}")
        return False

def test_excel_loading():
    """Test loading Excel format"""
    excel_paths = [
        "data/Refund_Claims_Data.xlsx",
        "data/customer_complaints.xlsx"
    ]
    
    for excel_path in excel_paths:
        if os.path.exists(excel_path):
            try:
                df = pd.read_excel(excel_path)
                print(f"✅ Excel Format Test PASSED")
                print(f"   - File: {excel_path}")
                print(f"   - Rows: {len(df)}")
                print(f"   - Columns: {list(df.columns)}")
                return True
            except Exception as e:
                print(f"❌ Excel Format Test FAILED: {str(e)}")
                return False
    
    print(f"⚠️  No Excel files found in data directory")
    return False

def test_required_columns():
    """Test that required columns exist"""
    required_cols = ['customer_name', 'order_id', 'complaint_text', 'complaint_date']
    
    csv_path = "data/Refund_Claims_Data.csv"
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            missing = [col for col in required_cols if col not in df.columns]
            if missing:
                print(f"❌ Column Test FAILED: Missing columns {missing}")
                return False
            else:
                print(f"✅ Column Test PASSED")
                print(f"   - All required columns present: {required_cols}")
                return True
        except Exception as e:
            print(f"❌ Column Test FAILED: {str(e)}")
            return False
    
    return False

if __name__ == "__main__":
    print("=" * 70)
    print("Testing File Format Support")
    print("=" * 70)
    
    results = []
    results.append(("CSV Loading", test_csv_loading()))
    results.append(("Excel Loading", test_excel_loading()))
    results.append(("Required Columns", test_required_columns()))
    
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All format tests passed! App is ready to run.")
    else:
        print("\n⚠️  Some tests failed. Please check your data files.")
