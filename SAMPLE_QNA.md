# Sample Questions and Application Responses

## 1. Pure RAG Query (Destination Knowledge)
**User:** What are the must-visit cultural neighbourhoods in Singapore?
**Assistant:** 
### Destination Facts (Knowledge Base)
Singapore features several vibrant cultural enclaves:
* **Chinatown:** A heritage district featuring the Buddha Tooth Relic Temple, Sri Mariamman Temple, and traditional shophouses [Source: Wikivoyage: Singapore Travel Guide | Link: https://en.wikivoyage.org/wiki/Singapore].
* **Little India:** Located along Serangoon Road, known for the Sri Veeramakaliamman Temple and the 24-hour Mustafa Centre [Source: Wikivoyage: Singapore Travel Guide | Link: https://en.wikivoyage.org/wiki/Singapore].
* **Kampong Glam:** The Malay-Arab historic district centered around the Sultan Mosque and Haji Lane [Source: Wikivoyage: Singapore Travel Guide | Link: https://en.wikivoyage.org/wiki/Singapore].

## 2. Standalone MCP Query (Live Data)
**User:** Convert my travel budget of INR 60000 to SGD.
**Assistant:**
### Current Data (MCP Tools)
[Live Data via MCP]: 60000.00 INR = 952.14 SGD (Live Rate: 1 INR = 0.0158 SGD)

## 3. Combined RAG and MCP Scenario (Required)
**User:** Create a three-day trip to Singapore and adjust the activities based on the weather forecast.
**Assistant:**
### Current Data (MCP Tools)
[Live Data via MCP] Current Singapore Temperature: 28.5°C, Wind: 12 km/h.
[Live Data via MCP] 3-Day Forecast for Singapore:
  • 2026-09-18: Max 31°C, Rain Probability 60% -> High rain probability (indoor activities advised)
  • 2026-09-19: Max 32°C, Rain Probability 20% -> Low rain probability (suitable for outdoor activities)
  • 2026-09-20: Max 30°C, Rain Probability 80% -> High rain probability (indoor activities advised)

### Destination Facts (Knowledge Base)
* **Indoor Attractions:** Cooled Conservatories at Gardens by the Bay (Flower Dome/Cloud Forest), Jewel Changi Airport, and the ArtScience Museum [Source: Visit Singapore: Things to Do | Link: https://www.visitsingapore.com/see-do-singapore/].
* **Outdoor Attractions:** Singapore Botanic Gardens, Sentosa Island Beaches [Source: Visit Singapore: Things to Do | Link: https://www.visitsingapore.com/see-do-singapore/].

### AI-Generated Recommendations
Based on the forecast, here is a weather-adjusted 3-day itinerary:
* **Day 1 (Rain likely):** Spend the day indoors at Jewel Changi Airport exploring the Rain Vortex, then head to the ArtScience Museum in the afternoon.
* **Day 2 (Clear skies):** Take advantage of the low rain probability by exploring the outdoor Singapore Botanic Gardens and relaxing at Palawan Beach on Sentosa Island.
* **Day 3 (Heavy rain expected):** Focus entirely on indoor attractions. Visit the Cooled Conservatories at Gardens by the Bay (Cloud Forest and Flower Dome).

## 4. Missing Knowledge Handling (Guardrail)
**User:** What are the best ski resorts in Singapore?
**Assistant:** NO_DATA_FOUND: The knowledge base does not contain sufficient information on this topic.
