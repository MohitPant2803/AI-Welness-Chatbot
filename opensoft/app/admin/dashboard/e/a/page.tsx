/* eslint-disable @next/next/no-img-element */
"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Avatar } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import {
  ArrowLeft,
  Search,
  AlertTriangle,
  Users,
  ChevronRight,
  Loader2,
  X,
} from "lucide-react";
import { baseURL, getMoodColor, getMoodIcon } from "@/lib/helperFunctions";

interface Employee {
  name: string;
  empid: string;
  dept: string;
  lastActive: string;
  currentMood: string;
  isEscalated: boolean;
  briefMoodSummary: string;
  avatarUrl: string;
}

interface ApiResponse {
  success: boolean;
  message: string;
  data: {
    _id: string;
    briefTotalUsersList: Employee[];
  };
  code: number;
}

export default function AllEmployeesPage() {
  const router = useRouter();
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedMoods, setSelectedMoods] = useState<string[]>([]);
  const [filteredEmployees, setFilteredEmployees] = useState<Employee[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Available mood filters
  const moodFilters = [
    { name: "Happy", color: "bg-green-100" },
    { name: "Tending to Happy", color: "bg-lime-100" },
    { name: "Neutral", color: "bg-gray-100" },
    { name: "Sad", color: "bg-red-100" },
    { name: "Angry", color: "bg-red-100" },
  ];

  // Fetch employees from API
  const fetchEmployees = async () => {
    try {
      const token = localStorage.getItem("token");

      const res = await fetch(baseURL + "/a/api/v1/admin/details/db/all", {
        method: "GET",
        headers: {
          Authorization: "Bearer " + token,
        },
      });
      const json: ApiResponse = await res.json();
      if (!res.ok) {
        throw new Error(json.message || "Failed to fetch employees");
      }
      // Use the briefTotalUsersList from the fetched data
      setEmployees(json.data.briefTotalUsersList);
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchEmployees();
  }, []);

  // Filter employees based on search query and selected moods
  useEffect(() => {
    let filtered = employees;

    // Filter by search query (checking name, empid, and department)
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(
        (employee) =>
          employee.name.toLowerCase().includes(query) ||
          employee.empid.toLowerCase().includes(query) ||
          employee.dept.toLowerCase().includes(query)
      );
    }

    // Filter by selected moods
    if (selectedMoods.length > 0) {
      filtered = filtered.filter((employee) =>
        selectedMoods.includes(employee.currentMood)
      );
    }

    setFilteredEmployees(filtered);
  }, [searchQuery, selectedMoods, employees]);

  // Toggle mood filter
  function toggleMoodFilter(mood: string) {
    if (selectedMoods.includes(mood)) {
      setSelectedMoods(selectedMoods.filter((m) => m !== mood));
    } else {
      setSelectedMoods([...selectedMoods, mood]);
    }
  }

  // Clear all filters
  function clearFilters() {
    setSearchQuery("");
    setSelectedMoods([]);
  }

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-blue-50 to-purple-50">
        <Loader2 className="text-primary h-12 w-12 animate-spin" />
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 pb-6">
      {/* Top Navigation Bar */}
      <nav className="fixed top-0 right-0 left-0 z-50 border-b border-gray-200 bg-white p-2 shadow-sm">
        <div className="mx-auto flex max-w-7xl items-center justify-between">
          <div className="flex flex-col">
            <div className="flex items-center gap-2">
              <Users className="h-6 w-6 text-black" />
              <h1 className="text-xl font-bold text-black">Admin Dashboard</h1>
            </div>
            <div
              onClick={() => router.push("/admin/dashboard")}
              className="flex w-full cursor-pointer items-center justify-end gap-2 text-sm text-gray-500"
            >
              <ArrowLeft className="h-4 w-4" />
              <span>Back to Dashboard</span>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => {
                localStorage.removeItem("token");
                router.push("/auth/signin");
              }}
              className="flex cursor-pointer items-center gap-2 font-bold"
            >
              <ArrowLeft className="h-4 w-4" />
              <span>Sign Out</span>
            </Button>
          </div>
        </div>
      </nav>

      <div className="mx-auto max-w-7xl px-4 pt-20 md:px-8">
        {/* Page Header */}
        <div className="mb-6 flex flex-col items-start justify-between md:flex-row md:items-center">
          <div>
            <h2 className="text-2xl font-bold text-gray-800">All Employees</h2>
            <p className="text-sm text-gray-600">
              View and manage all employee profiles
            </p>
          </div>
        </div>

        {/* Search and Filter Section */}
        <Card className="mb-6 rounded-xl border border-gray-100 bg-white p-4 shadow-sm">
          <div className="flex flex-col gap-4 md:flex-row">
            {/* Search Bar */}
            <div className="relative flex-grow">
              <Search className="absolute top-2.5 left-2.5 h-4 w-4 text-gray-500" />
              <Input
                type="search"
                placeholder="Search by name, ID, or department..."
                className="w-full border-gray-200 bg-white pl-8"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>

            <div className="flex items-center gap-2">
              <Button
                variant="outline"
                size="sm"
                className="flex cursor-pointer items-center gap-2 border-gray-200 font-bold text-gray-900"
                onClick={clearFilters}
                disabled={!searchQuery && selectedMoods.length === 0}
              >
                <X className="h-4 w-4" />
                <span>Clear Filters</span>
              </Button>
            </div>
          </div>

          {/* Mood Filters */}
          <div className="mt-4">
            <div className="mb-2 font-bold text-gray-800">Filter by mood:</div>
            <div className="flex flex-wrap gap-2">
              {moodFilters.map((mood) => {
                const isActive = selectedMoods.includes(mood.name);
                return (
                  <Badge
                    key={mood.name}
                    variant={isActive ? "default" : "outline"}
                    className={`cursor-pointer ${
                      isActive ? mood.color : ""
                    } rounded-2xl border-transparent text-sm`}
                    onClick={() => toggleMoodFilter(mood.name)}
                  >
                    {getMoodIcon(mood.name)}
                    <span className="ml-1">{mood.name}</span>
                  </Badge>
                );
              })}
            </div>
          </div>
        </Card>

        {/* Employee List */}
        <div className="space-y-4">
          {filteredEmployees.length === 0 ? (
            <Card className="rounded-xl border border-gray-100 bg-white p-8 text-center shadow-sm">
              <p className="text-gray-600">
                No employees match your search criteria.
              </p>
              <Button variant="link" onClick={clearFilters} className="mt-2">
                Clear filters
              </Button>
            </Card>
          ) : (
            filteredEmployees.map((employee) => (
              <Card
                key={employee.empid}
                className={`rounded-lg border p-4 shadow-sm ${
                  employee.isEscalated
                    ? "border-amber-200 bg-amber-50"
                    : "border-gray-200 bg-white"
                } `}
              >
                <div className="flex items-center gap-4">
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
                        className={`${getMoodColor(
                          employee.currentMood
                        )} cursor-pointer rounded-2xl border-transparent text-sm font-semibold`}
                      >
                        {getMoodIcon(employee.currentMood)}
                        <span className="ml-1">{employee.currentMood}</span>
                      </Badge>
                      {employee.isEscalated && (
                        <Badge
                          variant="outline"
                          className="cursor-pointer rounded-2xl border-transparent bg-amber-100 text-sm font-semibold text-amber-800"
                        >
                          <AlertTriangle className="mr-1 h-3 w-3" />
                          Escalated
                        </Badge>
                      )}
                    </div>

                    <div className="mt-1 flex flex-wrap items-center gap-2 text-sm text-gray-700">
                      <span>ID: {employee.empid}</span>
                      <span>•</span>
                      <span>{employee.dept}</span>
                      <span>•</span>
                      <span>Active {employee.lastActive}</span>
                    </div>

                    {employee.briefMoodSummary && (
                      <p className="mt-2 text-sm text-amber-700">
                        <AlertTriangle className="mr-1 inline-block h-4 w-4" />
                        {employee.briefMoodSummary}
                      </p>
                    )}
                  </div>

                  <Button
                    variant="ghost"
                    size="sm"
                    className="ml-auto"
                    onClick={() =>
                      router.push(`/admin/dashboard/e/${employee.empid}`)
                    }
                  >
                    <span className="sr-only cursor-pointer font-bold sm:not-sr-only sm:mr-2">
                      View Details
                    </span>
                    <ChevronRight className="h-4 w-4" />
                  </Button>
                </div>
              </Card>
            ))
          )}
        </div>

        {/* Results Summary */}
        <div className="mt-4 text-sm text-gray-500">
          Showing {filteredEmployees.length} of {employees.length} employees
        </div>
      </div>

      {/* Decorative background elements */}
      <div className="animate-blob fixed top-20 left-10 h-72 w-72 rounded-full bg-purple-200 opacity-30 mix-blend-multiply blur-3xl" />
      <div className="animate-blob animation-delay-2000 fixed top-40 right-10 h-72 w-72 rounded-full bg-yellow-200 opacity-30 mix-blend-multiply blur-3xl" />
      <div className="animate-blob animation-delay-4000 fixed bottom-20 left-40 h-72 w-72 rounded-full bg-pink-200 opacity-30 mix-blend-multiply blur-3xl" />
    </main>
  );
}
