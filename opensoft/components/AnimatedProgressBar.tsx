/* eslint-disable @typescript-eslint/no-unused-vars */
import React, { useState, useEffect } from "react";

interface AnimatedProgressBarProps {
  targetWidth: number;
  duration?: number;
  delay?: number;
  backgroundColor?: string;
  foregroundColor?: string;
}

const AnimatedProgressBar: React.FC<AnimatedProgressBarProps> = ({
  targetWidth,
  duration = 1000,
  delay = 0,
  backgroundColor = "bg-gray-200",
  foregroundColor = "bg-black",
}) => {
  const [width, setWidth] = useState(0);
  const [isAnimating, setIsAnimating] = useState(false);

  useEffect(() => {
    // Add a delay before starting the animation if specified
    const delayTimer = setTimeout(() => {
      setIsAnimating(true);
      let startTime: number | undefined;
      let animationFrameId: number;

      // Animation function
      const animate = (timestamp: DOMHighResTimeStamp) => {
        if (!startTime) startTime = timestamp;
        const progress = timestamp - startTime;

        // Calculate the current width based on progress
        const currentWidth = Math.min(
          (progress / duration) * targetWidth,
          targetWidth
        );

        setWidth(currentWidth);

        // Continue animation until we reach the target width
        if (progress < duration) {
          animationFrameId = requestAnimationFrame(animate);
        } else {
          setWidth(targetWidth); // Ensure we end exactly at the target width
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
    }, delay);

    return () => clearTimeout(delayTimer);
  }, [targetWidth, duration, delay]);

  return (
    <div className={`h-2 w-full rounded-full ${backgroundColor}`}>
      <div
        className={`h-2 rounded-full ${foregroundColor} transition-all duration-300 ease-out`}
        style={{ width: `${width}%` }}
      ></div>
    </div>
  );
};

export default AnimatedProgressBar;
