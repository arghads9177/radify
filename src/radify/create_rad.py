#!/usr/bin/env python


from crew import Radify


# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information


def generate(job_desc: str) -> str:
    """
    Run the crew and generate the RAD.
    """
    inputs = {
        "job_description": job_desc
    }
    
    try:
        response = Radify().crew().kickoff(inputs=inputs)
        # Extract final output string from CrewOutput
        if hasattr(response, "raw"):
            return response.raw
        elif hasattr(response, "output"):
            return response.output
        elif hasattr(response, "final_output"):
            return response.final_output
        else:
            return str(response)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


