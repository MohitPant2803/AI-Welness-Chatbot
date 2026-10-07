/* eslint-disable @next/next/no-img-element */
"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Avatar } from "@/components/ui/avatar";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import {
  ArrowLeft,
  Search,
  AlertTriangle,
  Users,
  Download,
  MessageSquare,
  AlertCircle,
  Smile,
  ChevronRight,
  Loader2,
} from "lucide-react";
import MoodChart from "@/components/MoodChart";
import { getMoodColor, getMoodIcon, baseURL } from "@/lib/helperFunctions";
import AnimatedCounter from "@/components/AnimatedCounter"; // Import the new component

interface EmployeeMoodDistribution {
  happy: number;
  tendingToHappy: number;
  neutral: number;
  sad: number;
  angry: number;
}

interface DailyParticipationEntry {
  date: string;
  numberOfParticipants: number;
}

export interface EscalatedEmployee {
  name: string;
  empid: string;
  dept: string;
  lastActive: string;
  currentMood: string;
  isEscalated: boolean;
  briefMoodSummary: string;
  avatarUrl: string;
}

export interface DashboardData {
  totalNumberOfEmp: number;
  noOfHappyEmp: number;
  noOfEscalatedIssues: number;
  totalChatInteractions: number;
  employeeMoodDistribution: EmployeeMoodDistribution;
  dailyChatParticipation: DailyParticipationEntry[];
  hikeFromPrevMonth: number;
  briefEscalatedUsersList: EscalatedEmployee[];
}

export default function AdminDashboard() {
  const router = useRouter();
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(
    null
  );
  const [isLoaded, setIsLoaded] = useState(false);

  const fetchData = async () => {
    try {
      const token = localStorage.getItem("token");
      const res = await fetch(baseURL + "/a/api/v1/admin/details/db", {
        method: "GET",
        headers: {
          Authorization: "Bearer " + token,
        },
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.error || "Fetching failed");
      }
      // Save the "data" field from the response into state.
      setDashboardData(data.data);

      // Add a slight delay to make the animation more noticeable
      setTimeout(() => {
        setIsLoaded(true);
      }, 100);
    } catch (error) {
      console.error(error);
      setIsLoaded(true); // Set to true even on error to avoid infinite loading
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  // Display a loading indicator while data is being fetched
  if (!dashboardData) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-blue-50 to-purple-50">
        <Loader2 className="text-primary h-12 w-12 animate-spin" />
      </div>
    );
  }

  // Derived values from the fetched data.
  const totalEmployees = dashboardData.totalNumberOfEmp;
  const happyEmployeesPercentage = Math.round(
    (dashboardData.noOfHappyEmp / totalEmployees) * 100
  );
  const escalatedIssues = dashboardData.noOfEscalatedIssues;
  const totalChatInteractions = dashboardData.totalChatInteractions;

  // Map the fetched daily participation data to our expected format.
  const dailyParticipation: { date: string; count: number }[] =
    dashboardData.dailyChatParticipation.map((entry) => ({
      date: new Date(entry.date).toISOString().split("T")[0],
      count: entry.numberOfParticipants,
    }));

  // Use the fetched escalated users list.
  const escalatedEmployees = dashboardData.briefEscalatedUsersList;

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
      {/* Top Navigation Bar */}
      <nav className="fixed top-0 right-0 left-0 z-50 border-b border-gray-200 bg-white p-4 shadow-sm">
        <div className="mx-auto flex max-w-7xl items-center justify-between">
          <div className="flex items-center gap-2">
            <Users className="h-6 w-6 text-black" />
            <h1 className="text-xl font-bold text-black">Admin Dashboard</h1>
          </div>
          <div className="flex items-center gap-4">
            {/* Mobile Search Toggle */}
            <div className="relative block md:hidden">
              <button
                aria-label="Open Search"
                className="p-2 text-gray-500 hover:text-gray-700 focus:outline-none"
              >
                <Search className="h-5 w-5" />
              </button>
            </div>
            {/* Desktop Search */}
            <div className="relative hidden w-64 md:block">
              <Search className="absolute top-2.5 left-2.5 h-4 w-4 text-gray-500" />
              <Input
                type="search"
                placeholder="Search employees..."
                className="w-full border-gray-200 bg-white pl-8"
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    const value = (e.target as HTMLInputElement).value;
                    router.push(
                      `/admin/dashboard/e/search?q=${encodeURIComponent(value)}`
                    );
                  }
                }}
              />
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => {
                localStorage.removeItem("token");
                router.push("/auth/signin");
              }}
              className="flex cursor-pointer items-center gap-2"
            >
              <ArrowLeft className="h-4 w-4" />
              <span>Sign Out</span>
            </Button>
          </div>
        </div>
      </nav>

      <div className="mx-auto max-w-7xl px-4 pt-20 md:px-8">
        {/* Dashboard Header */}
        <div className="mb-6 flex flex-col items-start justify-between gap-4 md:flex-row md:items-center">
          <div>
            <h2 className="text-2xl font-bold text-gray-800">
              Employee Wellness Overview
            </h2>
            <p className="text-sm text-gray-600">
              Monitor employee well-being and engagement
            </p>
          </div>
          <div className="flex flex-wrap gap-2">
            <Button
              variant="default"
              size="sm"
              className="flex cursor-pointer items-center gap-2 bg-black font-bold text-white"
              onClick={() => router.push("/admin/dashboard/e/a")}
            >
              <Users className="h-4 w-4" />
              <span>View All Employees</span>
            </Button>
            <a
              href={`${baseURL}/r/api/v1/get/report/all`}
              target="_blank"
              rel="noopener noreferrer"
            >
              <Button
                variant="outline"
                size="sm"
                className="flex cursor-pointer items-center gap-2 border-gray-300 bg-white shadow-xs"
              >
                <Download className="h-4 w-4" />
                <span>Export</span>
              </Button>
            </a>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="mb-6 grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-4">
          <Card className="rounded-xl border border-gray-100 bg-white p-4 shadow-sm">
            <div className="flex items-center gap-4">
              <div className="rounded-full bg-gray-100 p-3">
                <Users className="h-5 w-5 text-black" />
              </div>
              <div>
                <p className="text-sm text-gray-500">Total Employees</p>
                <h3 className="text-2xl font-bold text-gray-800">
                  {isLoaded ? (
                    <AnimatedCounter value={totalEmployees} duration={1500} />
                  ) : (
                    0
                  )}
                </h3>
              </div>
            </div>
          </Card>
          <Card className="rounded-xl border border-gray-100 bg-white p-4 shadow-sm">
            <div className="flex items-center gap-4">
              <div className="rounded-full bg-green-100 p-3">
                <Smile className="h-5 w-5 text-green-600" />
              </div>
              <div>
                <p className="text-sm text-gray-500">Happy Employees</p>
                <h3 className="text-2xl font-bold text-gray-800">
                  {isLoaded ? (
                    <AnimatedCounter
                      value={happyEmployeesPercentage}
                      duration={1800}
                      suffix="%"
                    />
                  ) : (
                    "0%"
                  )}
                </h3>
              </div>
            </div>
          </Card>
          <Card className="rounded-xl border border-gray-100 bg-white p-4 shadow-sm">
            <div className="flex items-center gap-4">
              <div className="rounded-full bg-red-100 p-3">
                <AlertCircle className="h-5 w-5 text-red-600" />
              </div>
              <div>
                <p className="text-sm text-gray-500">Escalated Cases</p>
                <h3 className="text-2xl font-bold text-gray-800">
                  {isLoaded ? (
                    <AnimatedCounter value={escalatedIssues} duration={1200} />
                  ) : (
                    0
                  )}
                </h3>
              </div>
            </div>
          </Card>
          <Card className="rounded-xl border border-gray-100 bg-white p-4 shadow-sm">
            <div className="flex items-center gap-4">
              <div className="rounded-full bg-blue-100 p-3">
                <MessageSquare className="h-5 w-5 text-blue-600" />
              </div>
              <div>
                <p className="text-sm text-gray-500">Chat Interactions</p>
                <h3 className="text-2xl font-bold text-gray-800">
                  {isLoaded ? (
                    <AnimatedCounter
                      value={totalChatInteractions}
                      duration={2000}
                    />
                  ) : (
                    0
                  )}
                </h3>
              </div>
            </div>
          </Card>
        </div>

        {/* Charts Section */}
        <div className="mb-6 grid grid-cols-1 gap-6 md:grid-cols-2">
          {/* Mood Distribution Chart */}
          <Card className="rounded-xl border border-gray-100 bg-white p-6 shadow-sm">
            <h3 className="text-lg font-semibold text-gray-800">
              Employee Mood Distribution
            </h3>
            <MoodChart values={dashboardData.employeeMoodDistribution} />
          </Card>

          {/* Daily Participation Chart */}
          <Card className="rounded-xl border border-gray-100 bg-white p-6 shadow-sm">
            <h3 className="mb-4 text-lg font-semibold text-gray-800">
              Daily Chat Participation
            </h3>
            <div className="overflow-x-auto pb-4">
              <div className="min-w-max">
                <div className="flex flex-col gap-2">
                  <div className="mb-1 flex justify-end text-xs text-gray-500">
                    <div className="w-8 text-center">Mon</div>
                    <div className="w-8 text-center">Wed</div>
                    <div className="w-8 text-center">Fri</div>
                  </div>
                  <div className="flex flex-wrap gap-1">
                    {dailyParticipation.map((dayData, index) => {
                      let bgColor = "bg-gray-100";
                      if (dayData.count === 0) bgColor = "bg-gray-100";
                      else if (dayData.count < 10) bgColor = "bg-blue-100";
                      else if (dayData.count < 20) bgColor = "bg-blue-200";
                      else if (dayData.count < 30) bgColor = "bg-blue-300";
                      else if (dayData.count < 40) bgColor = "bg-blue-400";
                      else bgColor = "bg-blue-500";

                      return (
                        <div
                          key={index}
                          className={`h-8 w-8 rounded-md ${bgColor} flex items-center justify-center transition-all hover:scale-110`}
                          title={`${dayData.count} interactions on ${dayData.date}`}
                        >
                          {dayData.count > 0 && (
                            <span className="text-xs font-medium">
                              {dayData.count > 40 ? "+" : ""}
                            </span>
                          )}
                        </div>
                      );
                    })}
                  </div>
                  <div className="mt-4 flex items-center justify-end gap-2">
                    <span className="text-xs text-gray-500">Interactions:</span>
                    <div className="h-6 w-6 rounded-md bg-gray-100" />
                    <div className="h-6 w-6 rounded-md bg-blue-100" />
                    <div className="h-6 w-6 rounded-md bg-blue-200" />
                    <div className="h-6 w-6 rounded-md bg-blue-300" />
                    <div className="h-6 w-6 rounded-md bg-blue-400" />
                    <div className="h-6 w-6 rounded-md bg-blue-500" />
                  </div>
                </div>
              </div>
            </div>
            <div className="mt-2">
              <p className="text-sm text-gray-600">
                <span className="font-medium">
                  {isLoaded ? (
                    <AnimatedCounter
                      value={totalChatInteractions}
                      duration={1800}
                    />
                  ) : (
                    0
                  )}
                </span>{" "}
                total interactions this month
                <span className="ml-2 text-green-600">
                  ↑{" "}
                  {isLoaded ? (
                    <AnimatedCounter
                      value={dashboardData.hikeFromPrevMonth}
                      duration={1500}
                    />
                  ) : (
                    0
                  )}
                  % from last month
                </span>
              </p>
            </div>
          </Card>
        </div>

        {/* Escalated Issues Section */}
        <Card className="mb-6 rounded-xl border border-gray-100 bg-white p-6 shadow-sm">
          <div className="mb-4 flex flex-col gap-2 sm:flex-row sm:items-center">
            <div className="flex items-center gap-2">
              <AlertTriangle className="h-5 w-5 text-amber-500" />
              <h3 className="text-lg font-semibold text-gray-800">
                Escalated Issues
              </h3>
            </div>
            <Badge
              variant="outline"
              className="ml-0 rounded-2xl border-transparent bg-amber-100 font-bold text-amber-800 sm:ml-2"
            >
              {isLoaded ? (
                <AnimatedCounter
                  value={escalatedEmployees.length}
                  duration={1000}
                />
              ) : (
                0
              )}{" "}
              Employees
            </Badge>
          </div>
          <div className="max-h-[500px] space-y-4 overflow-y-auto">
            {escalatedEmployees.map((employee) => (
              <Card
                key={employee.empid}
                className="rounded-xl border border-amber-200 bg-amber-50 p-4 shadow-sm"
              >
                <div className="flex flex-col items-start gap-4 sm:flex-row sm:items-center">
                  <Avatar className="h-12 w-12 border-2 border-white shadow-sm">
                    <img
                      src={employee.avatarUrl || "/placeholder.svg"}
                      alt={employee.name}
                    />
                  </Avatar>
                  <div className="flex-grow">
                    <div className="flex flex-wrap items-center gap-2">
                      <h4 className="font-semibold text-gray-800">
                        {employee.name}
                      </h4>
                      <Badge
                        className={
                          getMoodColor(employee.currentMood) +
                          " rounded-2xl text-sm"
                        }
                      >
                        {getMoodIcon(employee.currentMood)}
                        <span className="ml-1">{employee.currentMood}</span>
                      </Badge>
                    </div>
                    <div className="mt-1 flex flex-wrap items-center gap-2 text-sm text-gray-600">
                      <span>ID: {employee.empid}</span>
                      <span>•</span>
                      <span>{employee.dept}</span>
                      <span>•</span>
                      <span>
                        Active {new Date(employee.lastActive).toLocaleString()}
                      </span>
                    </div>
                    <p className="mt-2 text-sm text-amber-700">
                      <AlertTriangle className="mr-1 inline-block h-4 w-4" />
                      {employee.briefMoodSummary}
                    </p>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    className="ml-auto cursor-pointer"
                    onClick={() =>
                      router.push(`/admin/dashboard/e/${employee.empid}`)
                    }
                  >
                    <span className="sr-only font-bold sm:not-sr-only sm:mr-2">
                      View Details
                    </span>
                    <ChevronRight className="h-4 w-4" />
                  </Button>
                </div>
              </Card>
            ))}
          </div>
        </Card>
      </div>

      {/* Decorative background elements */}
      <div className="animate-blob fixed top-20 left-10 h-72 w-72 rounded-full bg-purple-200 opacity-30 mix-blend-multiply blur-3xl" />
      <div className="animate-blob animation-delay-2000 fixed top-40 right-10 h-72 w-72 rounded-full bg-yellow-200 opacity-30 mix-blend-multiply blur-3xl" />
      <div className="animate-blob animation-delay-4000 fixed bottom-20 left-40 h-72 w-72 rounded-full bg-pink-200 opacity-30 mix-blend-multiply blur-3xl" />
    </main>
  );
}
