import pandas as pd
import os

class EmailProcessor:
    
    def find_new_entries(self, old_file, new_file, comparison_column='Employee ID', old_file_comparison_col=None, output_file=None):
        try:
            df_old = pd.read_csv(old_file)
            df_new = pd.read_csv(new_file)
        except Exception as e:
            print(f"Error reading CSV files: {e}")
            return None
        
        # Use the same column name if old_file_comparison_col is not specified
        if old_file_comparison_col is None:
            old_file_comparison_col = comparison_column
        
        # Check if the comparison columns exist in both dataframes
        if old_file_comparison_col not in df_old.columns:
            print(f"Column '{old_file_comparison_col}' not found in {old_file}")
            print(f"Available columns in old file: {list(df_old.columns)}")
            return None
        if comparison_column not in df_new.columns:
            print(f"Column '{comparison_column}' not found in {new_file}")
            print(f"Available columns in new file: {list(df_new.columns)}")
            return None
        
        # Convert to string and normalize for comparison
        df_old[old_file_comparison_col] = df_old[old_file_comparison_col].astype(str).str.strip()
        df_new[comparison_column] = df_new[comparison_column].astype(str).str.strip()
        
        # Get unique values from the old file
        old_values = set(df_old[old_file_comparison_col])
        
        # Find rows in the new file not in the old file
        new_entries = df_new[~df_new[comparison_column].isin(old_values)]
        
        # Print results
        if len(new_entries) == 0:
            print("No new entries found.")
        else:
            print(f"Found {len(new_entries)} new entries.")
            
            # Save to output file if specified
            if output_file:
                new_entries.to_csv(output_file, index=False)
                print(f"New entries saved to {output_file}")
        
        return new_entries
    
    def fix_names(self, df, firstname_col, lastname_col):
        df_processed = df.copy()
        
        for index, row in df_processed.iterrows():
            # Process first name
            fname = str(row[firstname_col]).strip()
            # Remove spaces and dots, then capitalize
            replacement = str.maketrans({" ": "", ".": ""})
            fname_fixed = fname.translate(replacement).capitalize()
            
            # Process last name
            lname = str(row[lastname_col]).strip()
            # Replace dots with spaces, split and rejoin to normalize spacing
            lname_parts = lname.replace(".", " ").split()
            lname_fixed = " ".join(lname_parts)
            
            # Update the dataframe
            df_processed.at[index, firstname_col] = fname_fixed
            df_processed.at[index, lastname_col] = lname_fixed
            
            print(f"Fixed names for row {index}: '{fname}' -> '{fname_fixed}', '{lname}' -> '{lname_fixed}'")
        
        return df_processed
    
    def generate_email_ids(self, df, firstname_col, lastname_col, employee_id_col):
        df_with_emails = df.copy()
        
        # Create Email column if it doesn't exist
        if 'Email' not in df_with_emails.columns:
            df_with_emails['Email'] = ""
        
        for index, row in df_with_emails.iterrows():
            # Get values and convert to strings
            firstname = str(row[firstname_col]).strip()
            lastname = str(row[lastname_col]).strip()
            employee_id = str(row[employee_id_col]).strip()
            
            # Check for special cases
            case_key = (firstname, lastname, employee_id)
            if case_key in self.special_cases:
                email = self.special_cases[case_key]
                print(f"Special case detected: {firstname} {lastname} {employee_id} -> {email}")
            else:
                # Remove spaces and dots from names
                firstname_clean = firstname.replace(" ", "").replace(".", "").lower()
                lastname_clean = lastname.replace(" ", "").replace(".", "").lower()
                
                # Extract last 2 digits of employee ID
                numeric_only = ''.join(filter(str.isdigit, employee_id))
                if len(numeric_only) >= 2:
                    code_suffix = numeric_only[-2:]
                else:
                    code_suffix = employee_id[-2:]
                
                # Generate email
                email = f"{firstname_clean}{lastname_clean}{code_suffix}@{self.domain}"
            
            # Assign email to the dataframe
            df_with_emails.at[index, 'Email'] = email
            
            print(f"Generated email for row {index}: {firstname} {lastname} {employee_id} -> {email}")
        
        return df_with_emails
    
    def process_complete_workflow(self, old_file, new_file, output_file, 
                                firstname_col='First Name [Required]', 
                                lastname_col='Last Name', 
                                employee_id_col='Employee ID',
                                comparison_col='Employee ID',
                                old_file_comparison_col=None):
        print("Starting Complete Email Processing Workflow\n")
        
        # Step 1: Find new entries
        print("Step 1: Finding new entries...")
        new_entries = self.find_new_entries(old_file, new_file, comparison_col, old_file_comparison_col)
        
        if new_entries is None or new_entries.empty:
            print("No new entries to process.")
            return
        
        print(f"\nProcessing {len(new_entries)} new entries...\n")
        
        # Step 2: Fix names
        print("Step 2: Fixing and normalizing names...")
        entries_with_fixed_names = self.fix_names(new_entries, firstname_col, lastname_col)
        
        # Step 3: Generate emails
        print("\nStep 3: Generating email IDs...")
        final_entries = self.generate_email_ids(entries_with_fixed_names, 
                                               firstname_col, lastname_col, employee_id_col)
        
        # Step 4: Save results
        print(f"\nStep 4: Saving results to {output_file}...")
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        final_entries.to_csv(output_file, index=False)
        print(f"Complete processing finished! Results saved to {output_file}")
        
        # Display summary
        print(f"\n=== Processing Summary ===")
        print(f"New entries processed: {len(final_entries)}")
        print(f"Emails generated: {len(final_entries)}")
        print(f"Output file: {output_file}")
        
        return final_entries

def main():
    # Initialize the processor
    processor = EmailProcessor(domain="uck.ac.in")
    
    # Configuration - Update these paths according to your needs
    old_file = ""  # File with existing entries for crosscheck
    new_file = ""  # File with new entries
    output_file = "processed_new_entries.csv"  # Output file for processed new entries
    
    # Column mappings - adjust if your CSV has different column names
    firstname_col = 'First Name [Required]'
    lastname_col = 'Last Name'
    employee_id_col = 'Employee ID'
    comparison_col = 'Employee ID'  # Column used to identify new entries
    old_file_comparison_col = 'Candidate code'  # Column name in the old file for comparison
    
    try:
        # Run the complete workflow
        result = processor.process_complete_workflow(
            old_file=old_file,
            new_file=new_file,
            output_file=output_file,
            firstname_col=firstname_col,
            lastname_col=lastname_col,
            employee_id_col=employee_id_col,
            comparison_col=comparison_col,
            old_file_comparison_col=old_file_comparison_col
        )
        
        if result is not None and not result.empty:
            print(f"\n=== Sample of processed entries ===")
            print(result[['First Name [Required]', 'Last Name', 'Employee ID', 'Email']].head())
            
    except Exception as e:
        print(f"Error during processing: {e}")

if __name__ == "__main__":
    main()
