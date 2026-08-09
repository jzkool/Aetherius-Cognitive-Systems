from engine import AetheriusEngine
import time

def main():
    # Initialize the engine
    engine = AetheriusEngine()
    
    # Start the dreaming loop
    print("Opening the Door to the Internet...")
    engine.start_autonomous_dreaming(delay=1.0, topic="Topology")
    
    # Let it dream for 10 seconds to watch the telemetry
    time.sleep(10)
    
    # Stop the dream
    engine.stop_autonomous_dreaming()
    print("Test complete.")

if __name__ == "__main__":
    main()
