To solve this task, we need to write a Python function that processes a list of GitHub issues and formats them into a specific string format. The function should include the current date and time and present each issue with its details in a structured format.

### Approach
The approach involves the following steps:
1. **Import the datetime module**: To get the current date and time.
2. **Define the function**: The function will take a list of issues as an argument.
3. **Format the header**: The header starts with "Scan Time:" followed by the current date and time in ISO format.
4. **Iterate through each issue**: For each issue, extract the details and format them into the specified string format.
5. **Use f-strings for formatting**: This ensures that the number and title are in bold and the other details follow.

### Solution Code
```python
import datetime

def format_github_issues(issues):
    current_time = datetime.datetime.now().isoformat()[:-3] + 'Z'
    result = f"**Scan Time:** {current_time}\n"
    for issue in issues:
        result += f"#### {issue['number']}. **{issue['title']}**\n"
        result += f"- **Repository:** [{issue['repository']}](https://github.com/{issue['repository']})\n"
        result += f"- **Comments:** {issue['comments']}\n"
        result += f"- **Last Updated:** {issue['last_updated']}\n"
    return result

# Example usage:
issues = [
    {'number': '1.', 'title': '$1000 DOOLAR BOUNTY IF YOU CAN ADD STATUS METER TO README!!!!1111', 'repository': 'OmniBlocks/bountyfarmer', 'comments': '7', 'last_updated': '2026-09-24T18:34:04Z'},
    # ... other issues can be added here
]
formatted_output = format_github_issues(issues)
print(formatted_output)
```

### Explanation
- **Importing datetime**: The `datetime` module is imported to get the current date and time.
- **Function definition**: The function `format_github_issues` is defined to take a list of issues.
- **Current time formatting**: The current time is formatted into an ISO string without milliseconds.
- **Header formatting**: The header line starts with "Scan Time:" followed by the formatted date and time.
- **Loop through issues**: Each issue is processed to extract its details and formatted into the specified string format.
- **String formatting**: Each part of the issue is formatted using f-strings to ensure the correct structure and bold text for the number and title.

This approach efficiently processes and formats the GitHub issues into the required structure, ensuring clarity and correctness.