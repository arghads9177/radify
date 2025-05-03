from typing import List
from src.radify_api.crew import RadifyApiCrew



def generate_rad_text(text_input: str) -> str:
    """
    Main function to generate RAD text.
    """

    print(text_input)
    # Generate RAD using the combined text
    inputs = {
        'job_description': text_input
    }
    try:
        rad_text = RadifyApiCrew().crew().kickoff(inputs=inputs)
        print(f"Generated RAD text: {rad_text}")
    except Exception as e:
        print(f"Error during RAD generation: {e}")
        raise e
    return rad_text