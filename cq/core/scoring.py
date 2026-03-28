# Confidence Scoring Module

"""Confidence score calculation for knowledge units."""

import logging

logger = logging.getLogger(__name__)

# Minimum sample size for confidence calculation
MIN_SAMPLE_SIZE = 5

# Confidence bounds
MIN_CONFIDENCE = 0.1
MAX_CONFIDENCE = 1.0
DEFAULT_CONFIDENCE = 0.5


def calculate_confidence(
    helpful_count: int,
    not_helpful_count: int,
    usage_count: int = 0
) -> float:
    """Calculate confidence score based on feedback and usage.

    The formula uses a weighted approach:
    - Base confidence starts at 0.5
    - Feedback ratio (helpful - not_helpful) / max(total_feedback, MIN_SAMPLE_SIZE)
    - This ratio is scaled by 0.5 and added to the base
    - Result is clamped between MIN_CONFIDENCE and MAX_CONFIDENCE

    Args:
        helpful_count: Number of helpful feedback votes
        not_helpful_count: Number of not helpful feedback votes
        usage_count: Number of times the knowledge was used (for future use)

    Returns:
        Confidence score between 0.1 and 1.0

    Examples:
        >>> calculate_confidence(0, 0, 0)  # No feedback
        0.5
        >>> calculate_confidence(5, 0, 10)  # All positive
        1.0
        >>> calculate_confidence(0, 5, 10)  # All negative
        0.1
        >>> calculate_confidence(3, 2, 5)  # Mixed
        0.6
    """
    total_feedback = helpful_count + not_helpful_count

    # No feedback: return default confidence
    if total_feedback == 0:
        logger.debug("No feedback available, using default confidence")
        return DEFAULT_CONFIDENCE

    # Calculate feedback ratio
    # Use max(total_feedback, MIN_SAMPLE_SIZE) to reduce early volatility
    denominator = max(total_feedback, MIN_SAMPLE_SIZE)
    feedback_diff = helpful_count - not_helpful_count

    # Confidence = 0.5 + (feedback_diff / denominator) * 0.5
    # This gives:
    # - 0.5 baseline when feedback is balanced
    # - Up to 1.0 when all feedback is positive
    # - Down to 0.1 when all feedback is negative
    confidence = DEFAULT_CONFIDENCE + (feedback_diff / denominator) * 0.5

    # Clamp to valid range
    confidence = max(MIN_CONFIDENCE, min(MAX_CONFIDENCE, confidence))

    logger.debug(
        f"Calculated confidence: {confidence:.3f} "
        f"(helpful={helpful_count}, not_helpful={not_helpful_count}, "
        f"total={total_feedback}, usage={usage_count})"
    )

    return round(confidence, 3)


def calculate_confidence_from_stats(
    helpful_count: int,
    not_helpful_count: int,
    total_count: int,
    usage_count: int = 0
) -> float:
    """Calculate confidence from feedback statistics dict.

    Convenience function that accepts a stats dict from get_feedback_stats().

    Args:
        helpful_count: Number of helpful feedback votes
        not_helpful_count: Number of not helpful feedback votes
        total_count: Total feedback count (for validation)
        usage_count: Number of times the knowledge was used

    Returns:
        Confidence score between 0.1 and 1.0
    """
    # Validate counts match
    expected_total = helpful_count + not_helpful_count
    if total_count != expected_total:
        logger.warning(
            f"Feedback count mismatch: expected {expected_total}, "
            f"got {total_count}. Using derived counts."
        )

    return calculate_confidence(helpful_count, not_helpful_count, usage_count)
