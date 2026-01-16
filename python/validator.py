"""
Superstore Sales Analytics - Data Validation & Enhancement Layer
Author: Your Name
Description: Takes Excel-cleaned data, validates quality, adds enhancements, exports final CSV
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

class SuperstoreValidator:
    """Data validation and enhancement layer for pre-cleaned sales data"""
    
    def __init__(self, input_csv, output_csv='data/Superstore_Final_Cleaned.csv'):
        """
        Initialize validator
        
        Args:
            input_csv: Path to your Excel-cleaned CSV file
            output_csv: Path for final validated output (default: data/Superstore_Final_Cleaned.csv)
        """
        self.input_csv = input_csv
        self.output_csv = output_csv
        self.df = None
        self.validation_report = []
        self.insights_report = []
        
    def load_data(self):
        """Load Excel-cleaned CSV data"""
        print("📂 Loading Excel-cleaned data...")
        try:
            # Try cp1252 first (common Windows encoding), fallback to utf-8
            try:
                self.df = pd.read_csv(self.input_csv, encoding='cp1252')
            except:
                self.df = pd.read_csv(self.input_csv, encoding='utf-8')
            print(f"✅ Loaded {len(self.df):,} rows and {len(self.df.columns)} columns")
            return True
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False
    
    def validate_data(self):
        """Run comprehensive data quality checks"""
        print("\n🔍 Running data quality validation...")
        
        issues_found = 0
        
        # Check 1: Missing values
        missing = self.df.isnull().sum()
        if missing.any():
            self.validation_report.append(f"⚠️  Missing values detected:\n{missing[missing > 0]}")
            issues_found += 1
        else:
            self.validation_report.append("✅ No missing values")
        
        # Check 2: Duplicate Order IDs
        if 'Order ID' in self.df.columns:
            # Note: Same Order ID can appear multiple times for different products
            # Check for completely duplicate rows instead
            duplicates = self.df.duplicated().sum()
            if duplicates > 0:
                self.validation_report.append(f"⚠️  Found {duplicates} completely duplicate rows")
                issues_found += 1
            else:
                self.validation_report.append("✅ No duplicate rows")
        
        # Check 3: Negative sales values (data integrity issue)
        if 'Sales' in self.df.columns:
            negative_sales = (self.df['Sales'] < 0).sum()
            if negative_sales > 0:
                self.validation_report.append(f"⚠️  {negative_sales} rows with negative sales (possible data error)")
                issues_found += 1
            else:
                self.validation_report.append("✅ All sales values are non-negative")
        
        # Check 4: Date format consistency
        if 'Order Date' in self.df.columns:
            try:
                pd.to_datetime(self.df['Order Date'])
                self.validation_report.append("✅ Date format is consistent")
            except:
                self.validation_report.append("⚠️  Date format inconsistencies detected")
                issues_found += 1
        
        # Check 5: Discount range validation (0 to 1 or 0 to 100)
        if 'Discount' in self.df.columns:
            max_discount = self.df['Discount'].max()
            min_discount = self.df['Discount'].min()
            
            # Check if discounts are in decimal (0-1) or percentage (0-100) format
            if max_discount > 1:
                invalid = ((self.df['Discount'] < 0) | (self.df['Discount'] > 100)).sum()
            else:
                invalid = ((self.df['Discount'] < 0) | (self.df['Discount'] > 1)).sum()
            
            if invalid > 0:
                self.validation_report.append(f"⚠️  {invalid} rows with invalid discount values")
                issues_found += 1
            else:
                self.validation_report.append("✅ All discount values are within valid range")
        
        # Check 6: Sales-Profit relationship check
        if 'Sales' in self.df.columns and 'Profit' in self.df.columns:
            # Check for extreme profit margins (potential data errors)
            extreme_loss = (self.df['Profit'] / self.df['Sales'] < -2).sum()
            if extreme_loss > 0:
                self.validation_report.append(f"⚠️  {extreme_loss} rows with extreme losses (>200% negative margin)")
                issues_found += 1
        
        # Print validation summary
        print("\n" + "="*60)
        print("📋 DATA QUALITY VALIDATION REPORT")
        print("="*60)
        for item in self.validation_report:
            print(item)
        print("="*60)
        
        if issues_found == 0:
            print("✅ All quality checks passed!")
        else:
            print(f"⚠️  Found {issues_found} potential issues (review recommended)")
        
        return issues_found == 0
    
    def enhance_data(self):
        """Add calculated fields and enhancements"""
        print("\n🔧 Enhancing data with calculated fields...")
        
        enhancements_added = []
        
        # Enhancement 1: Time dimensions (if not already present)
        if 'Order Date' in self.df.columns:
            self.df['Order Date'] = pd.to_datetime(self.df['Order Date'])
            
            if 'Year' not in self.df.columns:
                self.df['Year'] = self.df['Order Date'].dt.year
                enhancements_added.append("Year")
            
            if 'Month' not in self.df.columns:
                self.df['Month'] = self.df['Order Date'].dt.month
                enhancements_added.append("Month")
            
            if 'Quarter' not in self.df.columns:
                self.df['Quarter'] = self.df['Order Date'].dt.quarter
                enhancements_added.append("Quarter")
            
            if 'Day of Week' not in self.df.columns:
                self.df['Day of Week'] = self.df['Order Date'].dt.day_name()
                enhancements_added.append("Day of Week")
            
            if 'Month Name' not in self.df.columns:
                self.df['Month Name'] = self.df['Order Date'].dt.month_name()
                enhancements_added.append("Month Name")
        
        # Enhancement 2: Profit Margin percentage
        if 'Sales' in self.df.columns and 'Profit' in self.df.columns:
            if 'Profit Margin' not in self.df.columns:
                self.df['Profit Margin'] = (self.df['Profit'] / self.df['Sales'] * 100).round(2)
                # Handle division by zero or infinity
                self.df['Profit Margin'] = self.df['Profit Margin'].replace([np.inf, -np.inf], 0)
                enhancements_added.append("Profit Margin (%)")
        
        # Enhancement 3: Discount Band categorization
        if 'Discount' in self.df.columns:
            if 'Discount Band' not in self.df.columns:
                self.df['Discount Band'] = pd.cut(
                    self.df['Discount'], 
                    bins=[0, 0.15, 0.31, 0.5, 1.0],
                    labels=['0-15%', '16-31%', '32-50%', '50%+'],
                    include_lowest=True
                )
                enhancements_added.append("Discount Band")
        
        # Enhancement 4: Sales Tier
        if 'Sales' in self.df.columns:
            if 'Sales Tier' not in self.df.columns:
                sales_quantiles = self.df['Sales'].quantile([0.33, 0.67])
                self.df['Sales Tier'] = pd.cut(
                    self.df['Sales'],
                    bins=[0, sales_quantiles[0.33], sales_quantiles[0.67], self.df['Sales'].max()],
                    labels=['Low', 'Medium', 'High'],
                    include_lowest=True
                )
                enhancements_added.append("Sales Tier")
        
        if enhancements_added:
            print(f"✅ Added {len(enhancements_added)} enhancement(s):")
            for enhancement in enhancements_added:
                print(f"   • {enhancement}")
        else:
            print("ℹ️  All enhancements already present in data")
        
        return enhancements_added
    
    def generate_insights(self):
        """Generate automated business insights"""
        print("\n📊 GENERATING AUTOMATED BUSINESS INSIGHTS")
        print("="*60)
        
        # Insight 1: Top loss-making sub-categories
        if 'Sub-Category' in self.df.columns and 'Profit' in self.df.columns:
            loss_makers = self.df.groupby('Sub-Category')['Profit'].sum().sort_values().head(3)
            print("\n🔴 Top 3 Loss-Making Sub-Categories:")
            self.insights_report.append("\n🔴 Top 3 Loss-Making Sub-Categories:")
            for cat, loss in loss_makers.items():
                line = f"   • {cat}: ${loss:,.2f}"
                print(line)
                self.insights_report.append(line)
        
        # Insight 2: Discount impact on profitability
        if 'Discount' in self.df.columns and 'Profit Margin' in self.df.columns:
            discount_bins = pd.cut(
                self.df['Discount'], 
                bins=[0, 0.15, 0.31, 0.5, 1.0],
                labels=['0-15%', '16-31%', '32-50%', '50%+'],
                include_lowest=True
            )
            margin_by_discount = self.df.groupby(discount_bins, observed=True)['Profit Margin'].mean()
            
            print("\n📉 Average Profit Margin by Discount Level:")
            self.insights_report.append("\n📉 Average Profit Margin by Discount Level:")
            for level, margin in margin_by_discount.items():
                status = "✅" if margin > 0 else "❌"
                line = f"   {status} {level}: {margin:.2f}%"
                print(line)
                self.insights_report.append(line)
        
        # Insight 3: Regional performance
        if 'Region' in self.df.columns:
            regional_perf = self.df.groupby('Region').agg({
                'Sales': 'sum',
                'Profit': 'sum'
            }).sort_values('Profit', ascending=False)
            
            print("\n🌎 Regional Performance (ranked by profit):")
            self.insights_report.append("\n🌎 Regional Performance (ranked by profit):")
            for region, row in regional_perf.iterrows():
                line = f"   • {region}: Sales ${row['Sales']:,.0f} | Profit ${row['Profit']:,.0f}"
                print(line)
                self.insights_report.append(line)
        
        # Insight 4: Category profitability
        if 'Category' in self.df.columns:
            category_perf = self.df.groupby('Category').agg({
                'Sales': 'sum',
                'Profit': 'sum',
                'Profit Margin': 'mean'
            }).sort_values('Profit', ascending=False)
            
            print("\n📦 Category Performance:")
            self.insights_report.append("\n📦 Category Performance:")
            for category, row in category_perf.iterrows():
                line = f"   • {category}: Sales ${row['Sales']:,.0f} | Profit ${row['Profit']:,.0f} | Avg Margin {row['Profit Margin']:.2f}%"
                print(line)
                self.insights_report.append(line)
        
        # Insight 5: High-volume, low-profit products (red flag)
        if 'Sub-Category' in self.df.columns and 'Quantity' in self.df.columns:
            subcat_analysis = self.df.groupby('Sub-Category').agg({
                'Quantity': 'sum',
                'Profit': 'sum'
            })
            # Find high-volume but negative profit sub-categories
            red_flags = subcat_analysis[(subcat_analysis['Quantity'] > subcat_analysis['Quantity'].quantile(0.5)) & 
                                       (subcat_analysis['Profit'] < 0)]
            
            if not red_flags.empty:
                print("\n⚠️  High-Volume but Loss-Making Sub-Categories:")
                self.insights_report.append("\n⚠️  High-Volume but Loss-Making Sub-Categories:")
                for subcat, row in red_flags.iterrows():
                    line = f"   • {subcat}: {int(row['Quantity'])} units sold but ${row['Profit']:,.2f} loss"
                    print(line)
                    self.insights_report.append(line)
        
        print("="*60)
    
    def export_data(self):
        """Export validated and enhanced data"""
        print(f"\n💾 Exporting final cleaned data to: {self.output_csv}")
        
        try:
            # Create output directory only if path contains directories
            output_dir = os.path.dirname(self.output_csv)
            if output_dir and output_dir != '':
                os.makedirs(output_dir, exist_ok=True)
            
            # Export to CSV
            self.df.to_csv(self.output_csv, index=False, encoding='utf-8')
            
            # Get file info
            file_size = os.path.getsize(self.output_csv) / 1024  # KB
            print(f"✅ Successfully exported {len(self.df):,} rows × {len(self.df.columns)} columns")
            print(f"✅ File size: {file_size:.2f} KB")
            print(f"✅ Location: {os.path.abspath(self.output_csv)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error exporting data: {e}")
            return False
    
    def save_report(self):
        """Save validation and insights to text report"""
        report_path = 'data/python_validation_report.txt'
        
        try:
            # Create data directory if it doesn't exist
            os.makedirs(os.path.dirname(report_path), exist_ok=True)
            
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write("="*70 + "\n")
                f.write("SUPERSTORE DATA VALIDATION & INSIGHTS REPORT\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*70 + "\n\n")
                
                f.write("INPUT FILE:\n")
                f.write(f"  {self.input_csv}\n\n")
                
                f.write("OUTPUT FILE:\n")
                f.write(f"  {self.output_csv}\n\n")
                
                f.write("DATA SUMMARY:\n")
                f.write(f"  Total rows: {len(self.df):,}\n")
                f.write(f"  Total columns: {len(self.df.columns)}\n\n")
                
                f.write("="*70 + "\n")
                f.write("VALIDATION RESULTS\n")
                f.write("="*70 + "\n")
                for item in self.validation_report:
                    f.write(item + "\n")
                
                f.write("\n" + "="*70 + "\n")
                f.write("AUTOMATED BUSINESS INSIGHTS\n")
                f.write("="*70 + "\n")
                for item in self.insights_report:
                    f.write(item + "\n")
                
                f.write("\n" + "="*70 + "\n")
                f.write("NEXT STEPS:\n")
                f.write("="*70 + "\n")
                f.write("1. Review this validation report\n")
                f.write("2. Import the final CSV into SQLite using your existing SQL scripts\n")
                f.write("3. Refresh your Power BI dashboard\n")
                f.write("="*70 + "\n")
            
            print(f"✅ Validation report saved: {report_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving report: {e}")
            return False
    
    def run(self):
        """Execute the validation and enhancement pipeline"""
        print("="*70)
        print("🚀 SUPERSTORE DATA VALIDATOR - STARTING")
        print("="*70)
        print(f"Input: {self.input_csv}")
        print(f"Output: {self.output_csv}")
        print("="*70 + "\n")
        
        # Step 1: Load Excel-cleaned data
        if not self.load_data():
            return False
        
        # Step 2: Validate data quality
        self.validate_data()
        
        # Step 3: Add enhancements
        self.enhance_data()
        
        # Step 4: Generate business insights
        self.generate_insights()
        
        # Step 5: Export final CSV
        if not self.export_data():
            return False
        
        # Step 6: Save report
        self.save_report()
        
        print("\n" + "="*70)
        print("✅ VALIDATION COMPLETE!")
        print("="*70)
        print(f"\n📁 Final cleaned CSV: {self.output_csv}")
        print("📁 Validation report: data/python_validation_report.txt")
        print("\n📋 NEXT STEPS:")
        print("   1. Review the validation report")
        print("   2. Load final CSV into SQLite (your existing process)")
        print("   3. Refresh Power BI dashboard")
        print("="*70 + "\n")
        
        return True


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================
if __name__ == "__main__":
    # CONFIGURATION: Paths relative to project root
    # Assumes script is run from project root: python python/validator.py
    INPUT_FILE = "data/Superstore Cleaned.csv"          # Excel-cleaned input
    OUTPUT_FILE = "data/Superstore_Final_Cleaned.csv"   # Python-validated output
    
    # Run the validator
    validator = SuperstoreValidator(INPUT_FILE, OUTPUT_FILE)
    success = validator.run()
    
    if success:
        print("✨ Ready for SQL ingestion!")
    else:
        print("❌ Validation failed. Please check errors above.")