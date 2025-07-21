# Email Generator

A Python tool that automates the process of finding new student entries, fixing name formatting, and generating standardized email IDs for educational institutions.

## Features

- **New Entry Detection**: Compare CSV files to identify new students
- **Name Normalization**: Fix and standardize name formatting
- **Email Generation**: Create standardized email IDs using institutional format
- **Special Case Handling**: Support custom email formats for specific cases

## Installation

**Prerequisites**: Python 3.7+ and pandas

```bash
git clone https://github.com/yourusername/email-generator.git
cd email-generator
pip install pandas
```

## Usage

```python
from EmailGenerator import EmailProcessor

# Initialize and process
processor = EmailProcessor(domain="uck.ac.in")
result = processor.process_complete_workflow(
    old_file="existing_students.csv",
    new_file="new_applications.csv", 
    output_file="generated_emails.csv"
)
```

Or run directly:
```bash
python Email-Generator.py
```

## Configuration

Update file paths in `main()` function:

```python
old_file = "existing_students.csv"        # File with existing entries
new_file = "new_applications.csv"         # File with new entries  
output_file = "generated_emails.csv"      # Output file
```

### Required CSV Columns:
- `First Name [Required]` - Student's first name
- `Last Name` - Student's last name  
- `Employee ID` - Unique student identifier

## Email Format

Generated email format: `[firstname][lastname][last2digits]@[domain]`

**Examples:**
- John Doe, ID: 413***4001 → `johndoe01@uck.ac.in`
- Mary Jane Smith, ID: 416***4095 → `maryjanesmith95@uck.ac.in`

**Name Processing:**
- Removes spaces and dots from names
- Converts to lowercase
- Uses last 2 digits of student ID

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

**Built for educational institutions managing student data**
