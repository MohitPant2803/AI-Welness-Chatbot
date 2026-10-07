import React, { useState, useEffect } from "react";

// This component will animate a number counting up from 0 to the target value
interface AnimatedCounterProps {
  value: number;
  duration?: number;
  suffix?: string;
}

export const AnimatedCounter = ({ value, duration = 1000, suffix = "" }: AnimatedCounterProps) => {
  const [count, setCount] = useState(0);

  useEffect(() => {
    if (value === 0) {
      setCount(0);
      return;
    }

    // Animation logic
    let startTime: number | undefined;
    let animationFrameId: number;

    // Animation function
    const animate = (timestamp: DOMHighResTimeStamp) => {
      if (!startTime) startTime = timestamp;
      const progress = timestamp - startTime;

      // Calculate the current count based on progress
      const currentCount = Math.min(
        Math.floor((progress / duration) * value),
        value
      );

      setCount(currentCount);

      // Continue animation until we reach the target value
      if (progress < duration) {
        animationFrameId = requestAnimationFrame(animate);
      } else {
        setCount(value); // Ensure we end exactly at the target value
      }
    };

    // Start the animation
    animationFrameId = requestAnimationFrame(animate);

    // Cleanup function
    return () => {
      if (animationFrameId) {
        cancelAnimationFrame(animationFrameId);
      }
    };
  }, [value, duration]);

  return (
    <>
      {count}
      {suffix}
    </>
  );
};

export default AnimatedCounter;
