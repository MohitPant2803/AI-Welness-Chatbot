"use client";
import React from "react";

export function MoodCalendar({
  moodCalendar,
}: {
  moodCalendar: { moodLevel: number; timestamp: string }[];
}) {
  // Sort mood entries by timestamp (newest first)
  const sortedEntries = [...moodCalendar].sort(
    (a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
  );

  // Determine the reference date (today or the most recent entry)
  const today = new Date();
  const referenceDate = sortedEntries.length
    ? new Date(sortedEntries[0].timestamp)
    : today;

  // Calculate the date 149 days ago from the reference date
  const startDate = new Date(referenceDate);
  startDate.setDate(startDate.getDate() - 149);

  // Create an array of 150 days from startDate to referenceDate
  const daysArray = [];
  for (let i = 0; i < 150; i++) {
    const currentDate = new Date(startDate);
    currentDate.setDate(startDate.getDate() + i);
    daysArray.push(currentDate);
  }

  // Build a map of date strings to the last mood entry for that date.
  const moodMap: Record<string, { moodLevel: number; timestamp: string }> = {};
  moodCalendar.forEach((entry) => {
    const entryDate = new Date(entry.timestamp);
    // Convert entry date to UTC date string.
    const dateStr = new Date(
      Date.UTC(
        entryDate.getFullYear(),
        entryDate.getMonth(),
        entryDate.getDate()
      )
    )
      .toISOString()
      .split("T")[0];
    // Override so that the last entry for the day wins.
    moodMap[dateStr] = entry;
  });

  return (
    <div className="mx-auto grid w-full max-w-6xl grid-cols-20 gap-2">
      {daysArray.map((date) => {
        // Build the ISO date string for the current day using UTC.
        const dateStr = new Date(
          Date.UTC(date.getFullYear(), date.getMonth(), date.getDate())
        )
          .toISOString()
          .split("T")[0];

        const entry = moodMap[dateStr];

        // Default background is grey for missing data.
        let bgColor = "bg-gray-100";
        let displayValue = "";

        if (entry && entry.moodLevel) {
          const level = entry.moodLevel;
          if (level === 1) bgColor = "bg-red-200";
          else if (level === 2) bgColor = "bg-yellow-200";
          else if (level === 3) bgColor = "bg-green-200";
          else if (level === 4) bgColor = "bg-emerald-300";
          else if (level === 5) bgColor = "bg-blue-200";
          displayValue = level.toString();
        }

        // Format the date for display in the title
        const formattedDate = `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, "0")}-${date.getDate().toString().padStart(2, "0")}`;

        return (
          <div
            key={dateStr}
            className={`h-10 w-10 rounded-md ${bgColor} flex items-center justify-center transition-all hover:scale-110`}
            title={
              entry
                ? `Mood level: ${entry.moodLevel} on ${formattedDate}`
                : `No data for ${formattedDate}`
            }
          >
            {displayValue}
          </div>
        );
      })}
    </div>
  );
}
