## Architecture Diagram
---
<img src="static/Architecture.jpg" alt="Diagram" width="800" height="600">

## ER Diagram
---
<img src="static/ERdiagram.jpg" alt="Diagram" width="800" height="600">

## Sequence Diagram
---
<img src="static/sequenceDiagram.jpg" alt="Diagram" width="800" height="600">

### Sequence of Actions

1. *User Actions:*
   - Requests forecast data.
   - Enters savings goal details, expense details, and income details.

2. *UI Actions:*
   - Sends forecast request to the server.
   - Submits savings goal, expense data, and income data.

3. *Server Actions:*
   - Processes requests, interacts with Python scripts, and communicates with Snowflake.
   - Returns forecast data and confirmation messages to the UI.

4. *Python Script Actions:*
   - Processes data and interacts with Snowflake for data storage and retrieval.
   - Returns processed data and confirmation messages to the server.

5. *Snowflake Actions:*
   - Handles queries and data insertion.
   - Confirms data insertion and returns queried data.

## Conclusion

This high-level design document provides an overview of the SmartSaver application's architecture, including the main components, their interactions, and detailed diagrams. This document will evolve as the project progresses, incorporating additional details and refinements. The accompanying README.md ensures that users and developers can easily set up and understand the project.
