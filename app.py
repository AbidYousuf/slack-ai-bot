from flask import Flask, request, jsonify
import requests
import threading
import json
import csv
from io import StringIO
from ask_engine import ask_database
import urllib.parse

app = Flask(__name__)

# Store last query result globally (simple MVP storage)
last_rows = []


def format_rows(rows):
    if not rows:
        return "No results found."

    formatted = "```\n"
    for row in rows:
        formatted += f"{row[0]:<10} | {row[1]}\n"
    formatted += "```"
    return formatted


def generate_csv(rows):
    output = StringIO()
    writer = csv.writer(output)

    writer.writerow(["Column1", "Column2"])
    for row in rows:
        writer.writerow(row)

    return output.getvalue()

def generate_chart_url(rows):
    if not rows or len(rows[0]) != 2:
        return None

    labels = [str(row[0]) for row in rows]
    values = [float(row[1]) for row in rows]

    chart_config = {
        "type": "line",
        "data": {
            "labels": labels,
            "datasets": [{
                "label": "Revenue",
                "data": values,
                "fill": False
            }]
        }
    }

    encoded = urllib.parse.quote(json.dumps(chart_config))
    return f"https://quickchart.io/chart?c={encoded}"

def background_task(question, response_url):
    global last_rows

    try:
        sql, rows = ask_database(question)
        last_rows = rows

        # Show chart only if query includes date range
        show_chart = "between" in sql.lower() or "date" in sql.lower()

        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Query Result:*"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": format_rows(rows)
                }
            }
        ]

        # Add chart only if valid date query and 2-column result
        if show_chart and rows and len(rows[0]) == 2:
            chart_url = generate_chart_url(rows)

            blocks.append({
                "type": "image",
                "image_url": chart_url,
                "alt_text": "Date Range Chart"
            })

        # Add Export CSV button
        blocks.append({
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Export CSV"
                    },
                    "action_id": "export_csv"
                }
            ]
        })

        message = {
            "response_type": "in_channel",
            "blocks": blocks
        }

        requests.post(response_url, json=message)

    except Exception as e:
        error_message = {
            "response_type": "ephemeral",
            "text": f"```{str(e)}```"
        }
        requests.post(response_url, json=error_message)

@app.route("/slack", methods=["POST"])
def slack_handler():
    global last_rows

    # 🔹 If button clicked
    if request.form.get("payload"):
        payload = json.loads(request.form["payload"])

        if payload["actions"][0]["action_id"] == "export_csv":

            csv_content = generate_csv(last_rows)
            response_url = payload["response_url"]

            message = {
            "response_type": "ephemeral",
            "text": f"```{csv_content}```"
            }

            requests.post(response_url, json=message)

            return "", 200

    # 🔹 Normal slash command
    question = request.form.get("text")
    response_url = request.form.get("response_url")

    threading.Thread(
        target=background_task,
        args=(question, response_url),
        daemon=True
    ).start()

    return jsonify({
        "response_type": "ephemeral",
        "text": "Processing your query..."
    })


if __name__ == "__main__":
    app.run(port=3000, threaded=True)