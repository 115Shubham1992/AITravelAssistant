import os
import shutil
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

DOCUMENTS_DIR = "./data"
PERSIST_DIR = "./chroma_db"

SAMPLE_SOURCES = {
    "wikivoyage_singapore.txt": {
        "title": "Wikivoyage: Singapore Travel Guide",
        "url": "https://en.wikivoyage.org/wiki/Singapore",
        "content": """
Singapore is a city-state in Southeast Asia consisting of the main island and 63 surrounding islets.

Neighbourhoods & Cultural Enclaves:
- Chinatown: Heritage district featuring the Buddha Tooth Relic Temple, Sri Mariamman Temple, and traditional shophouses. Excellent street food at Chinatown Complex Food Centre and Maxwell Food Centre.
- Little India: Vibrant enclave along Serangoon Road. Key attractions: Sri Veeramakaliamman Temple, colourful shophouses, and the 24-hour retail giant Mustafa Centre.
- Kampong Glam: Malay-Arab historic district centered around the golden-domed Sultan Mosque and trendy Haji Lane, famous for indie fashion boutiques, cafes, and street art murals.
- Civic District & Marina Bay: Home to Marina Bay Sands, Merlion Park, Esplanade Theatres, and the Singapore Flyer.

Transportation Guidance:
The Mass Rapid Transit (MRT) is the fastest and most efficient way to travel across the island. Visitors can use contactless Mastercard, Visa, or mobile wallets (Apple Pay/Google Pay) directly at station turnstiles, or buy a reloadable EZ-Link transit card. An extensive public bus network complements the MRT. Metered taxis and ride-hailing services (Grab) are widely accessible.
"""
    },
    "visitsingapore_essentials.txt": {
        "title": "Visit Singapore: Essential Travel Information",
        "url": "https://www.visitsingapore.com/travel-guide-tips/essential-travel-information/",
        "content": """
Practical Visitor Information:
- Climate: Tropical, warm, and humid year-round. Average daily temperatures range from 26°C to 32°C. Afternoon showers and sudden thunderstorms are common.
- Currency: Singapore Dollar (SGD). Cards and digital payments are accepted across retail and restaurants, though physical cash is recommended for hawker centres.
- Drinking Water: Tap water is strictly potable, meeting WHO standards.
- Local Laws & Etiquette: Strict penalties apply for littering and jaywalking. The importation and sale of chewing gum is prohibited. Smoking is restricted to designated yellow boxes. Tipping is not customary, as bills typically include a 10% service charge and prevailing GST.
- Connectivity: Tourists can purchase physical or eSIM tourist cards at Changi Airport or convenience stores. Free islandwide public Wi-Fi is accessible via the Wireless@SGx network.
"""
    },
    "visitsingapore_things_to_do.txt": {
        "title": "Visit Singapore: Things to Do, Food & Family Guide",
        "url": "https://www.visitsingapore.com/see-do-singapore/",
        "content": """
Food & Local Hawker Culture:
Singapore's UNESCO-inscribed Hawker Culture offers world-class dining at modest prices:
- Iconic Dishes: Hainanese Chicken Rice, Chili Crab, Katong Laksa, Char Kway Teow, Roti Prata, and Satay.
- Popular Food Centres: Maxwell Food Centre (famous for Tian Tian Chicken Rice), Lau Pa Sat (known for outdoor evening Satay Street), and Chinatown Complex Food Centre.

Activities for Families with Children:
- Mandai Wildlife Reserve: Includes the world-renowned open-concept Singapore Zoo, Night Safari (tram journey through nocturnal wildlife habitats), and Bird Paradise.
- Sentosa Island: Offers Universal Studios Singapore, S.E.A. Aquarium (home to over 100,000 marine animals), and Skyline Luge Sentosa.
- Singapore Botanic Gardens: Features the Jacob Ballas Children's Garden, Asia's first garden dedicated to youth education.
- Science Centre Singapore: Interactive STEM exhibits and an indoor snow play center (Snow City).

Indoor Attractions (Rainy Day / Midday Heat Alternatives):
- Cooled Conservatories at Gardens by the Bay: Flower Dome and Cloud Forest (featuring an indoor waterfall and mist walk).
- Jewel Changi Airport: Features the 40-meter indoor HSBC Rain Vortex waterfall and Canopy Park.
- ArtScience Museum at Marina Bay: Features interactive digital art installations (Future World exhibition).
- National Gallery Singapore: Houses the premier public collection of modern Southeast Asian art.
- S.E.A. Aquarium at Resorts World Sentosa.

Outdoor Attractions (Clear Weather):
- Supertree Grove & OCBC Skyway at Gardens by the Bay.
- Singapore Botanic Gardens (UNESCO World Heritage Site).
- Southern Ridges & Henderson Waves walking trails.
- Sentosa Island Beaches (Siloso Beach, Palawan Beach).
"""
    },
    "visitsingapore_itineraries.txt": {
        "title": "Visit Singapore: Sample Itineraries",
        "url": "https://www.visitsingapore.com/itineraries/",
        "content": """
Suggested 3-Day Sightseeing Itinerary:
- Day 1: Futuristic Marina Bay & Waterfront.
  Morning: Walk along Merlion Park and Marina Bay waterfront promenade.
  Afternoon: Explore Gardens by the Bay (Flower Dome & Cloud Forest).
  Evening: Watch the Spectra Light and Water Show at Marina Bay Sands, followed by dinner at Lau Pa Sat Satay Street.
- Day 2: Cultural Enclaves & Heritage.
  Morning: Chinatown heritage walking tour, Buddha Tooth Relic Temple, and lunch at Chinatown Complex.
  Afternoon: Explore Little India along Serangoon Road and browse Mustafa Centre.
  Evening: Walk through Kampong Glam, visit Sultan Mosque, and dine on Haji Lane.
- Day 3: Wildlife & Island Adventure.
  Morning: Visit Singapore Zoo or Sentosa Island.
  Afternoon: Indoor exploration at S.E.A. Aquarium or ArtScience Museum if afternoon showers occur.
  Evening: Dinner at a hawker centre and night views from the Marina Bay Sands SkyPark Observation Deck.
"""
    }
}

def setup_knowledge_base():
    if os.path.exists(PERSIST_DIR):
        shutil.rmtree(PERSIST_DIR)
        print("Removed previous Chroma database.")

    os.makedirs(DOCUMENTS_DIR, exist_ok=True)
    raw_docs = []

    for filename, data in SAMPLE_SOURCES.items():
        filepath = os.path.join(DOCUMENTS_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(data["content"])

        raw_docs.append(
            Document(
                page_content=data["content"],
                metadata={"source_title": data["title"], "source_url": data["url"]}
            )
        )

    splitter = RecursiveCharacterTextSplitter(chunk_size=450, chunk_overlap=80)
    chunked_docs = splitter.split_documents(raw_docs)

    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-2-preview")
    vector_store = Chroma.from_documents(
        documents=chunked_docs,
        embedding=embeddings,
        persist_directory=PERSIST_DIR
    )
    print(f"Successfully ingested {len(chunked_docs)} chunks into ChromaDB at {PERSIST_DIR}")

if __name__ == "__main__":
    setup_knowledge_base()
