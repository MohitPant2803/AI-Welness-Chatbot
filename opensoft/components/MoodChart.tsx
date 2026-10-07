/* eslint-disable @typescript-eslint/no-explicit-any */
import React from "react";
import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
} from "recharts";

interface MoodValues {
  happy: number;
  neutral: number;
  tendingToHappy: number;
  sad: number;
  angry: number;
}

interface MoodChartProps {
  values?: MoodValues;
}

const RADIAN = Math.PI / 180;

const renderCustomizedLabel = ({
  cx,
  cy,
  midAngle,
  innerRadius,
  outerRadius,
  percent,
}: any) => {
  const radius = innerRadius + (outerRadius - innerRadius) / 2;
  const x = cx + radius * Math.cos(-midAngle * RADIAN);
  const y = cy + radius * Math.sin(-midAngle * RADIAN);

  return (
    <text
      x={x}
      y={y}
      fill="#333"
      textAnchor="middle"
      dominantBaseline="middle"
      className="text-sm font-bold"
    >
      {`${(percent * 100).toFixed(0)}%`}
    </text>
  );
};

export default function MoodChart({ values }: MoodChartProps) {
  // Map the values prop to the data array. Fallback to default values if not provided.
  const data = [
    { name: "Happy", value: values?.happy ?? 45, color: "#4ade80" },
    { name: "Neutral", value: values?.neutral ?? 30, color: "#94a3b8" },
    {
      name: "Tending to Happy",
      value: values?.tendingToHappy ?? 15,
      color: "#a3e635",
    },
    { name: "Sad", value: values?.sad ?? 7, color: "#fb7185" },
    { name: "Angry", value: values?.angry ?? 3, color: "#f43f5e" },
  ];

  return (
    <div className="flex w-full">
      <ResponsiveContainer width="100%" height={400}>
        <PieChart>
          <Pie
            data={data}
            dataKey="value"
            cx="50%"
            cy="50%"
            innerRadius="55%"
            outerRadius="90%"
            labelLine={false}
            label={renderCustomizedLabel}
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip
            formatter={(value: any, name: any) => [`${value}`, name]}
            contentStyle={{ fontSize: "0.85rem" }}
          />
          <Legend
            verticalAlign="bottom"
            height={60}
            wrapperStyle={{
              fontSize: "0.85rem",
              marginTop: "50px",
              alignContent: "center",
            }}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
