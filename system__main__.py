import argparse
import logging
from research_coordinator import ResearchCoordinator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    parser = argparse.ArgumentParser(description="AI Research Coordinator")
    parser.add_argument("url", help="URL of the research paper to analyze")
    args = parser.parse_args()

    coordinator = ResearchCoordinator()
    coordinator.process_paper(args.url)

if __name__ == "__main__":
    main()
