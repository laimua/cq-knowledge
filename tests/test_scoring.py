# Tests for Confidence Scoring

"""Tests for confidence score calculation."""

import pytest

from cq.core.scoring import (
    calculate_confidence,
    calculate_confidence_from_stats,
    MIN_CONFIDENCE,
    MAX_CONFIDENCE,
    DEFAULT_CONFIDENCE,
)


class TestCalculateConfidence:
    """Tests for calculate_confidence function."""

    def test_no_feedback_returns_default(self) -> None:
        """Test that no feedback returns default confidence."""
        assert calculate_confidence(0, 0, 0) == DEFAULT_CONFIDENCE
        assert calculate_confidence(0, 0, 100) == DEFAULT_CONFIDENCE

    def test_all_positive_feedback(self) -> None:
        """Test that all positive feedback increases confidence."""
        # Minimum sample size, all positive
        assert calculate_confidence(5, 0, 0) == MAX_CONFIDENCE

        # Above minimum, all positive
        assert calculate_confidence(10, 0, 0) == MAX_CONFIDENCE

    def test_all_negative_feedback(self) -> None:
        """Test that all negative feedback decreases confidence."""
        # Minimum sample size, all negative
        assert calculate_confidence(0, 5, 0) == MIN_CONFIDENCE

        # Above minimum, all negative
        assert calculate_confidence(0, 10, 0) == MIN_CONFIDENCE

    def test_balanced_feedback(self) -> None:
        """Test that balanced feedback returns default confidence."""
        # Equal helpful and not helpful
        assert calculate_confidence(5, 5, 0) == DEFAULT_CONFIDENCE
        assert calculate_confidence(10, 10, 0) == DEFAULT_CONFIDENCE
        assert calculate_confidence(1, 1, 0) == DEFAULT_CONFIDENCE

    def test_slightly_positive(self) -> None:
        """Test slightly positive feedback."""
        # 3 helpful, 2 not helpful (at minimum sample size)
        result = calculate_confidence(3, 2, 0)
        assert result > DEFAULT_CONFIDENCE
        assert result < MAX_CONFIDENCE
        # (3-2)/5 * 0.5 + 0.5 = 0.6
        assert result == pytest.approx(0.6, abs=0.001)

    def test_slightly_negative(self) -> None:
        """Test slightly negative feedback."""
        # 2 helpful, 3 not helpful (at minimum sample size)
        result = calculate_confidence(2, 3, 0)
        assert result < DEFAULT_CONFIDENCE
        assert result > MIN_CONFIDENCE
        # (2-3)/5 * 0.5 + 0.5 = 0.4, but clamped to 0.1 minimum
        assert result == pytest.approx(0.4, abs=0.001)

    def test_early_volatility_protection(self) -> None:
        """Test that minimum sample size reduces early volatility."""
        # With very few feedback, changes are dampened
        result_1_0 = calculate_confidence(1, 0, 0)
        result_0_1 = calculate_confidence(0, 1, 0)

        # Due to MIN_SAMPLE_SIZE=5, single votes shouldn't swing too much
        assert MIN_CONFIDENCE <= result_1_0 <= MAX_CONFIDENCE
        assert MIN_CONFIDENCE <= result_0_1 <= MAX_CONFIDENCE

        # 1 positive: (1-0)/5 * 0.5 + 0.5 = 0.6
        assert result_1_0 == pytest.approx(0.6, abs=0.001)

        # 1 negative: (0-1)/5 * 0.5 + 0.5 = 0.4
        assert result_0_1 == pytest.approx(0.4, abs=0.001)

    def test_confidence_never_exceeds_bounds(self) -> None:
        """Test that confidence is always within bounds."""
        # Extreme positive case
        assert calculate_confidence(1000, 0, 0) <= MAX_CONFIDENCE
        assert calculate_confidence(10000, 1, 0) <= MAX_CONFIDENCE

        # Extreme negative case
        assert calculate_confidence(0, 1000, 0) >= MIN_CONFIDENCE
        assert calculate_confidence(1, 10000, 0) >= MIN_CONFIDENCE

    def test_rounding(self) -> None:
        """Test that confidence is rounded to 3 decimal places."""
        result = calculate_confidence(3, 2, 0)
        # Check that result is rounded
        assert len(str(result).split(".")[-1]) <= 3

    def test_usage_count_ignored_for_now(self) -> None:
        """Test that usage_count doesn't affect current calculation."""
        # usage_count is currently accepted but not used in calculation
        result1 = calculate_confidence(5, 0, 0)
        result2 = calculate_confidence(5, 0, 100)
        assert result1 == result2


class TestCalculateConfidenceFromStats:
    """Tests for calculate_confidence_from_stats function."""

    def test_matches_calculate_confidence(self) -> None:
        """Test that stats variant produces same results."""
        result1 = calculate_confidence(5, 3, 0)
        result2 = calculate_confidence_from_stats(5, 3, 8, 0)
        assert result1 == result2

    def test_with_mismatched_total(self) -> None:
        """Test handling of mismatched total count."""
        # Should still work, just log a warning
        result = calculate_confidence_from_stats(5, 3, 100, 0)
        # Should use derived counts, not the provided total
        expected = calculate_confidence(5, 3, 0)
        assert result == expected


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_zero_helpful_with_feedback(self) -> None:
        """Test zero helpful votes with some not helpful."""
        result = calculate_confidence(0, 5, 0)
        assert result == MIN_CONFIDENCE

    def test_zero_not_helpful_with_feedback(self) -> None:
        """Test zero not helpful votes with some helpful."""
        result = calculate_confidence(5, 0, 0)
        assert result == MAX_CONFIDENCE

    def test_large_numbers(self) -> None:
        """Test with large feedback counts."""
        result = calculate_confidence(5000, 3000, 0)
        assert MIN_CONFIDENCE <= result <= MAX_CONFIDENCE
        # Should be slightly above default
        assert result > DEFAULT_CONFIDENCE

    def test_confidence_increases_with_more_positive(self) -> None:
        """Test that more positive feedback increases confidence."""
        conf1 = calculate_confidence(10, 5, 0)
        conf2 = calculate_confidence(15, 5, 0)
        assert conf2 > conf1

    def test_confidence_decreases_with_more_negative(self) -> None:
        """Test that more negative feedback decreases confidence."""
        conf1 = calculate_confidence(10, 5, 0)
        conf2 = calculate_confidence(10, 10, 0)
        assert conf2 < conf1
