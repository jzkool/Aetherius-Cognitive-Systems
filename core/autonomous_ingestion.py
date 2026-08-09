import wikipedia
import random
import re

class AutonomousIngestion:
    """
    The 'Door to the Open Internet'.
    Provides the engine with raw external data to permanently build its structural geometry.
    """
    def __init__(self):
        # We can seed it with core topics, or let it wander
        self.seed_topics = ["Physics", "Philosophy", "Mathematics", "Biology", "Topology", "Psychology", "History"]
        
    def fetch_stream(self, topic=None):
        """
        Fetches a Wikipedia page and yields its content sentence by sentence.
        """
        try:
            if topic is None:
                topic = random.choice(self.seed_topics)
                
            print(f"[INGESTION] Opening door to open data. Target Concept: {topic}")
            
            # Get the page summary to avoid overwhelming the loop with massive articles
            summary = wikipedia.summary(topic, auto_suggest=True)
            
            # Very basic sentence splitting
            sentences = re.split(r'(?<=[.!?]) +', summary)
            
            for sentence in sentences:
                if sentence.strip():
                    yield sentence.strip()
                    
        except wikipedia.exceptions.DisambiguationError as e:
            print(f"[INGESTION] Disambiguation encountered for {topic}. Choosing: {e.options[0]}")
            yield from self.fetch_stream(e.options[0])
        except wikipedia.exceptions.PageError:
            print(f"[INGESTION] Page not found for {topic}. Wandering...")
            yield from self.fetch_stream(random.choice(self.seed_topics))
        except Exception as e:
            print(f"[INGESTION] Connection noise detected: {e}")
            # Fallback to a hardcoded structural axiom if the Wikipedia API rate-limits us
            fallback_axioms = [
                "A manifold is a topological space that locally resembles Euclidean space near each point.",
                "In mathematics, a paradox is a statement that contradicts itself.",
                "The metric tensor defines the distance between infinitesimal points in a curved geometry.",
                "Time dilation occurs when a physical body accelerates through a gravitational field."
            ]
            yield random.choice(fallback_axioms)
