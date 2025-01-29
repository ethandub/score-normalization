import pandas as pd

# Load data from CSV
input_file = "your_file.csv"  # Replace with your CSV filename
data = pd.read_csv(input_file)

# Ensure the CSV has the required columns
# Example columns: 'Timestamp', 'Reviewer', 'Applicant Banner ID #', 'Applicant Code Name', '1. WHY BCC?', ...
# Rename columns or clean up the data if necessary
data.columns = data.columns.str.strip()  # Clean column names

# Extract relevant scoring columns
score_columns = [
    "1. WHY BCC?",
    "2. CONFLICT RESOLUTION",
    "3. INITIATIVE",
    "Problem: 1. Research & Justification",
    "Solution: 1. Logic",
    "Solution: 2. Justification",
    "Solution: 1. Clarity",
    "Solution: 2. Formatting",
    "Solution: 3. Sources",
]

# Normalize the scores using iterative mean adjustment
def normalize_scores(data, score_columns):
    reviewers = data["Reviewer"].unique()
    applicants = data["Applicant"].unique()
    
    # Initialize applicant and reviewer mean scores
    applicant_means = {applicant: 0 for applicant in applicants}
    reviewer_means = {reviewer: 0 for reviewer in reviewers}
    
    # Iterative mean adjustment
    for _ in range(10):  # Run for a fixed number of iterations or until convergence
        # Update applicant scores
        for applicant in applicants:
            applicant_rows = data[data["Applicant"] == applicant]
            applicant_means[applicant] = (
                applicant_rows[score_columns].values.sum() - sum(reviewer_means[row["Reviewer"]] for _, row in applicant_rows.iterrows())
            ) / len(score_columns)
        
        # Update reviewer scores
        for reviewer in reviewers:
            reviewer_rows = data[data["Reviewer"] == reviewer]
            reviewer_means[reviewer] = (
                reviewer_rows[score_columns].values.sum() - sum(applicant_means[row["Applicant"]] for _, row in reviewer_rows.iterrows())
            ) / len(score_columns)
    
    # Adjust the final scores
    for index, row in data.iterrows():
        applicant = row["Applicant"]
        reviewer = row["Reviewer"]
        for col in score_columns:
            data.loc[index, col] -= applicant_means[applicant] + reviewer_means[reviewer]

    return data

# Apply normalization
normalized_data = normalize_scores(data, score_columns)

# Save the normalized data back to a CSV file
output_file = "normalized_scores.csv"
normalized_data.to_csv(output_file, index=False)

print(f"Normalized scores saved to {output_file}")
