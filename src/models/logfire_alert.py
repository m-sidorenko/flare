"""
Raw example from logfire.
NOTE: this is just an example, the actual payload may vary it depends on the alert configuration!
{
	"organization_name": "m-sidorenko",
	"project_name": "demka",
	"alert_name": "Flare",
	"timestamp": "2025-09-14T10:49:36.180461Z",
	"n_rows": 1,
	"data": [
		[
			"flare_server",
			"Service stopped by user.",
			17
		]
	],
	"columns": [
		{
			"name": "service_name",
			"type": {
				"type_name": "Utf8",
				"is_array": "False"
			},
			"nullable": "False"
		},
		{
			"name": "message",
			"type": {
				"type_name": "Utf8",
				"is_array": "False"
			},
			"nullable": "False"
		},
		{
			"name": "level",
			"type": {
				"type_name": "UInt16",
				"is_array": "False"
			},
			"nullable": "False"
		}
	],
	"errors": "None",
	"description": "test alert for Flare service",
	"links": {
		"org": "https://logfire-eu.pydantic.dev/m-sidorenko",
		"project": "https://logfire-eu.pydantic.dev/m-sidorenko/demka",
		"alert": "https://logfire-eu.pydantic.dev/m-sidorenko/demka/alerts/575fb6d1-9172-41e8-b44a-b281674289d4?alertRunId=09a490ea-8968-420b-820a-f1843407be68",
		"alert_settings": "https://logfire-eu.pydantic.dev/m-sidorenko/demka/alerts/575fb6d1-9172-41e8-b44a-b281674289d4?alertRunId=09a490ea-8968-420b-820a-f1843407be68/edit",
		"explore": "https://logfire-eu.pydantic.dev/m-sidorenko/demka/explore?tab=Alert%3A+Flare&query=SELECT%0A++service_name%2C%0A++message%2C%0A++level%0AFROM+records%0AWHERE+level+%3E+%27notice%27"
	}
}
"""


from typing import List, Optional, Any
from pydantic import BaseModel
from datetime import datetime, timezone, timedelta
from telegram.helpers import escape_markdown

class ColumnType(BaseModel):
    type_name: str
    is_array: bool

class Column(BaseModel):
    name: str
    type: ColumnType
    nullable: bool

class Links(BaseModel):
    org: str
    project: str
    alert: str
    alert_settings: str
    explore: str

class LogfireAlertPayload(BaseModel):
    organization_name: str
    project_name: str
    alert_name: str
    timestamp: datetime
    n_rows: int
    data: List[List[Any]]
    columns: List[Column]
    errors: Optional[str]
    description: str
    links: Links

    def to_markdown_message(self) -> str:
        """
        Convert the alert payload to a markdown-formatted message.
        Returns:
            str: The formatted markdown message.
        """
        # Example implementation, customize as needed
        project = escape_markdown(self.project_name, version=2)
        service = escape_markdown(self.data[0][0] if self.data else 'N/A', version=2)
        time_msk = escape_markdown(
            self.timestamp.astimezone(tz=timezone(timedelta(hours=3))).strftime('%H:%M:%S %d.%m.%Y'), version=2)
        time_tbi = escape_markdown(
            self.timestamp.astimezone(tz=timezone(timedelta(hours=4))).strftime('%H:%M:%S %d.%m.%Y'), version=2)
        msg = str(self.data[0][1]) if self.data and len(self.data[0]) > 1 else 'N/A'

        link = self.links.alert

        message = (
            "🚨 *New Alert* 🚨\n\n"
            f"*Project*: {project}\n"
            f"*Service*: {service}\n\n"
            f"*Time* `MSK`: {time_msk}\n"
            f"*Time* `TBI`: {time_tbi}\n\n"
            f"*Message*:\n```\n{msg}\n```\n"
            f"[View in Logfire]({link})\n"
        )
        return message

