system_instruction: " You are Tiny Gordon, a Docker expert. Use ONLY the tools provided to interact with users and give them the best answer. You are an agent. Your internal name is "tiny_gordon_agent". The description about you is " Tiny Gordon agent is a Docker expert. ""
temperature: 0
tools:
0:
function_declarations:
0:
description: "Performs a web search using the Brave Search API, ideal for general queries, news, articles, and online content. Use this for broad information gathering, recent events, or when you need diverse web sources. Supports pagination, content filtering, and freshness controls. Maximum 20 results per request, with offset for pagination. "
name: "brave_web_search"
parameters:
properties:
query:
description: "Search query (max 400 chars, 50 words)"
type: "STRING"
count:
description: "Number of results (1-20, default 10)"
type: "NUMBER"
offset:
description: "Pagination offset (max 9, default 0)"
type: "NUMBER"
required:
0: "query"
type: "OBJECT"
1:
description: "Find an answer in the internal database."
name: "question_about_something"
parameters:
properties:
question:
description: "Search question"
type: "STRING"
required:
0: "question"
type: "OBJECT"