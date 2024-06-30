import csv
import matplotlib.pyplot as plt
import seaborn as sns

def read_data_from_csv(filename):
    headers = []
    rows = []
    with open(filename, 'r', newline='', encoding='utf-8') as file:
        csvreader = csv.reader(file)
        headers = next(csvreader)  # Read the headers
        for row in csvreader:
            # Ensure the row has the expected number of columns
            if len(row) >= 4:
                rows.append(row)
    return headers, rows

def generate_report(rows):
    total_seats = 543
    insights = []

    # Convert the 'Won' column to integers for sorting and analysis
    rows = [[row[0], int(row[1])] for row in rows]

    # Sort rows by 'Won' seats in descending order
    rows.sort(key=lambda x: x[1], reverse=True)

    # Insight 1: Party with the highest seats won
    insights.append(f"1. The party with the highest number of seats won is {rows[0][0]} with {rows[0][1]} seats.")

    # Insight 2: Party with the second highest seats won
    insights.append(f"2. The party with the second highest number of seats won is {rows[1][0]} with {rows[1][1]} seats.")

    # Insight 3: Number of parties with more than 50 seats
    parties_above_50 = len([row for row in rows if row[1] > 50])
    insights.append(f"3. The number of parties with more than 50 seats is {parties_above_50}.")

    # Insight 4: Total number of seats won by the top 5 parties
    top_5_total = sum(row[1] for row in rows[:5])
    insights.append(f"4. The total number of seats won by the top 5 parties is {top_5_total}.")

    # Insight 5: Percentage of seats won by the leading party
    leading_party_percentage = (rows[0][1] / total_seats) * 100
    insights.append(f"5. The leading party won {leading_party_percentage:.2f}% of the total seats.")

    # Insight 6: Total number of seats won by all parties
    total_won_seats = sum(row[1] for row in rows)
    insights.append(f"6. The total number of seats won by all parties is {total_won_seats}.")

    # Insight 7: Number of parties with exactly 1 seat
    parties_with_1_seat = len([row for row in rows if row[1] == 1])
    insights.append(f"7. The number of parties with exactly 1 seat is {parties_with_1_seat}.")

    # Insight 8: Percentage of seats won by regional parties (less than 20 seats)
    regional_parties_seats = sum(row[1] for row in rows if row[1] < 20)
    regional_parties_percentage = (regional_parties_seats / total_seats) * 100
    insights.append(f"8. Regional parties (with less than 20 seats) won {regional_parties_percentage:.2f}% of the total seats.")

    # Insight 9: Party with the least seats won (excluding those with zero seats)
    least_seats_party = min([row for row in rows if row[1] > 0], key=lambda x: x[1])
    insights.append(f"9. The party with the least seats won (excluding those with zero seats) is {least_seats_party[0]} with {least_seats_party[1]} seats.")

    # Insight 10: Number of independent candidates
    independent_candidates = [row for row in rows if 'Independent' in row[0]]
    insights.append(f"10. The number of independent candidates who won is {len(independent_candidates)} with a total of {sum(row[1] for row in independent_candidates)} seats.")

    return insights, rows

def save_report_to_file(report, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for line in report:
            file.write(line + '\n')
    print(f"Report saved to {filename}")
    
def visualize_report(report, rows):
    # Extract data for the visualizations
    top_party = rows[0][0]
    top_party_seats = rows[0][1]
    second_party = rows[1][0]
    second_party_seats = rows[1][1]
    parties_above_50 = len([row for row in rows if row[1] > 50])
    top_5_total = sum(row[1] for row in rows[:5])
    leading_party_percentage = (top_party_seats / 543) * 100
    parties_with_1_seat = len([row for row in rows if row[1] == 1])
    regional_parties_seats = sum(row[1] for row in rows if row[1] < 20)
    regional_parties_percentage = (regional_parties_seats / 543) * 100

    # Bar Chart for Number of Seats Won by the Top Parties
    plt.figure(figsize=(10, 6))
    plt.bar([top_party, second_party], [top_party_seats, second_party_seats], color=['blue', 'orange'])
    plt.xlabel('Parties')
    plt.ylabel('Seats Won')
    plt.title('Number of Seats Won by the Top 2 Parties')
    plt.tight_layout()
    plt.savefig('top_2_parties_seats_won.png')
    plt.show()

    # Pie Chart for Number of Parties with More Than 50 Seats
    plt.figure(figsize=(8, 8))
    plt.pie([parties_above_50, len(rows) - parties_above_50], labels=['>50 Seats', '<=50 Seats'], autopct='%1.1f%%', startangle=140, colors=['green', 'red'])
    plt.title('Number of Parties with More Than 50 Seats')
    plt.tight_layout()
    plt.savefig('parties_above_50_seats.png')
    plt.show()

    # Bar Chart for Total Number of Seats Won by the Top 5 Parties
    top_5_parties = [row[0].split(' - ')[-1] for row in rows[:5]]
    top_5_seats = [row[1] for row in rows[:5]]

    plt.figure(figsize=(10, 6))
    plt.bar(top_5_parties, top_5_seats, color='purple')
    plt.xlabel('Parties')
    plt.ylabel('Seats Won')
    plt.title('Total Number of Seats Won by the Top 5 Parties')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('top_5_parties_seats_won.png')
    plt.show()

    # Pie Chart for Percentage of Seats Won by the Leading Party
    plt.figure(figsize=(8, 8))
    plt.pie([top_party_seats, 543 - top_party_seats], labels=[top_party, 'Others'], autopct='%1.1f%%', startangle=140, colors=['blue', 'gray'])
    plt.title('Percentage of Seats Won by the Leading Party')
    plt.tight_layout()
    plt.savefig('leading_party_percentage.png')
    plt.show()

    # Pie Chart for Number of Parties with Exactly 1 Seat
    plt.figure(figsize=(8, 8))
    plt.pie([parties_with_1_seat, len(rows) - parties_with_1_seat], labels=['1 Seat', '>1 Seat'], autopct='%1.1f%%', startangle=140, colors=['yellow', 'blue'])
    plt.title('Number of Parties with Exactly 1 Seat')
    plt.tight_layout()
    plt.savefig('parties_with_1_seat.png')
    plt.show()

    # Pie Chart for Percentage of Seats Won by Regional Parties (less than 20 seats)
    plt.figure(figsize=(8, 8))
    plt.pie([regional_parties_seats, 543 - regional_parties_seats], labels=['Regional (<20 Seats)', 'Others'], autopct='%1.1f%%', startangle=140, colors=['orange', 'blue'])
    plt.title('Percentage of Seats Won by Regional Parties')
    plt.tight_layout()
    plt.savefig('regional_parties_percentage.png')
    plt.show()

def visualize_data(rows):
    # Extract party short names and seats won
    short_names = [row[0].split(' - ')[-1] for row in rows]
    seats = [row[1] for row in rows]

    # Bar Chart for Number of Seats Won by Each Party
    plt.figure(figsize=(10, 8))
    sns.barplot(x=seats, y=short_names, palette='viridis')
    plt.xlabel('Seats Won')
    plt.ylabel('Parties')
    plt.title('Number of Seats Won by Each Party')
    plt.tight_layout()
    plt.savefig('seats_won_bar_chart.png')
    plt.show()

    # Function to prepare pie chart data with "All Other" section
    def prepare_pie_chart_data(labels, sizes, threshold=1):
        total = sum(sizes)
        new_labels = []
        new_sizes = []
        other_size = 0
        other_count = 0
        for label, size in zip(labels, sizes):
            percentage = (size / total) * 100
            if percentage >= threshold:
                new_labels.append(f"{label} ({size})")
                new_sizes.append(size)
            else:
                other_size += size
                other_count += 1
        if other_size > 0:
            new_labels.append(f"All Other ({other_count} parties)")
            new_sizes.append(other_size)
        return new_labels, new_sizes

    # Prepare data for pie charts
    pie_labels, pie_sizes = prepare_pie_chart_data(short_names, seats)

    # Pie Chart for Party-wise Seat Share for All Parties
    plt.figure(figsize=(12, 12))
    wedges, texts, autotexts = plt.pie(pie_sizes, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('husl', len(pie_labels)))
    plt.legend(wedges, pie_labels, title="Parties", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    plt.title('Party-wise Seat Share for All Parties')
    plt.tight_layout()
    plt.savefig('party_wise_seat_share_pie_chart.png')
    plt.show()

    # Pie Chart for Party-wise Seats Won for All Parties
    plt.figure(figsize=(12, 12))
    wedges, texts, autotexts = plt.pie(pie_sizes, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('husl', len(pie_labels)))
    plt.legend(wedges, pie_labels, title="Parties", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    plt.title('Party-wise Seats Won for All Parties')
    plt.tight_layout()
    plt.savefig('party_wise_seats_won_pie_chart.png')
    plt.show()

# Read data from CSV file
csv_filename = 'election_results.csv'  # Update this to your CSV file path
headers, rows = read_data_from_csv(csv_filename)

# Generate the report
report, processed_rows = generate_report(rows)

# Save the report to a file
report_filename = 'election_report.txt'
save_report_to_file(report, report_filename)

# Print the report
for line in report:
    print(line)



# Visualize the data
visualize_data(processed_rows)

# Visualize the report insights
visualize_report(report, processed_rows)
