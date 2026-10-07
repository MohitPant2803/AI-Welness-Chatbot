/* eslint-disable @next/next/no-img-element */
"use client";

import { useState, useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Avatar } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { ArrowLeft, ChevronRight } from "lucide-react";
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

export default function SearchResultsPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const query = searchParams.get("q") || "";
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchSearchResults = async () => {
      try {
        const token = localStorage.getItem("token");
        if (!token) {
          router.push("/auth/signin");
          return;
        }

        const response = await fetch(
          `${baseURL}/a/api/v1/admin/details/search/${encodeURIComponent(query)}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (!response.ok) {
          throw new Error("Failed to fetch search results");
        }

        const data = await response.json();

        // Transform API response to match our existing Employee interface
        interface ApiResult {
          name: string;
          empid: string;
          dept: string;
          lastActive: string;
          currentVibe?: string;
          briefMoodSummary?: string;
          avatar?: string;
        }

        const transformedResults: Employee[] = data.results.map(
          (result: ApiResult) => ({
            name: result.name,
            empid: result.empid,
            dept: result.dept,
            lastActive: result.lastActive,
            currentMood: result.currentVibe || "neutral",
            isEscalated: false, // Add logic if available in API
            briefMoodSummary: result.briefMoodSummary || "",
            avatarUrl: result.avatar || "/placeholder.svg",
          })
        );

        setEmployees(transformedResults);
        setError(null);
      } catch (err) {
        setError(
          err instanceof Error ? err.message : "Failed to fetch results"
        );
      } finally {
        setIsLoading(false);
      }
    };

    if (query) {
      fetchSearchResults();
    }
  }, [query, router]);

  if (isLoading) {
    return <div className="p-4 text-center">Loading...</div>;
  }

  if (error) {
    return (
      <Card className="m-4 p-4 text-center text-red-500">
        Error: {error}
        <Button onClick={() => window.location.reload()} className="mt-2">
          Retry
        </Button>
      </Card>
    );
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 pb-6">
      <nav className="fixed top-0 right-0 left-0 z-50 border-b border-gray-200 bg-white p-2 shadow-sm">
        <div className="mx-auto flex max-w-7xl items-center justify-between">
          <div className="flex items-center gap-2">
            <Button
              variant="ghost"
              onClick={() => router.push("/admin/dashboard")}
              className="flex cursor-pointer items-center gap-2"
            >
              <ArrowLeft className="h-4 w-4" />
              Back to Dashboard
            </Button>
          </div>
        </div>
      </nav>

      <div className="mx-auto max-w-7xl px-4 pt-20 md:px-8">
        <h2 className="mb-6 text-2xl font-bold text-gray-800">
          Search Results for &quot;{query}&quot;
        </h2>

        <div className="space-y-4">
          {employees.length === 0 ? (
            <Card className="rounded-xl border border-gray-100 bg-white p-8 text-center shadow-sm">
              <p className="text-gray-600">No matching employees found.</p>
            </Card>
          ) : (
            employees.map((employee) => (
              <Card
                key={employee.empid}
                className={`rounded-lg border p-4 shadow-sm ${
                  employee.isEscalated
                    ? "border-amber-200 bg-amber-50"
                    : "border-gray-200 bg-white"
                }`}
              >
                <div className="flex items-center gap-4">
                  <Avatar className="h-12 w-12 border-2 border-white shadow-sm">
                    <img
                      src={employee.avatarUrl}
                      alt={employee.name}
                      className="object-cover"
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
                        )} rounded-2xl border-transparent text-sm font-semibold`}
                      >
                        {getMoodIcon(employee.currentMood)}
                        <span className="ml-1">{employee.currentMood}</span>
                      </Badge>
                    </div>

                    <div className="mt-1 flex flex-wrap items-center gap-2 text-sm text-gray-700">
                      <span>ID: {employee.empid}</span>
                      <span>•</span>
                      <span>{employee.dept}</span>
                      <span>•</span>
                      <span>
                        Last active:{" "}
                        {new Date(employee.lastActive).toLocaleDateString()}
                      </span>
                    </div>

                    {employee.briefMoodSummary && (
                      <div className="mt-2 text-sm">
                        <span className="text-black">Mood Summary: </span>
                        <span className="text-gray-600">
                          {employee.briefMoodSummary}
                        </span>
                      </div>
                    )}
                  </div>

                  <Button
                    variant="ghost"
                    size="sm"
                    className="ml-auto cursor-pointer"
                    onClick={() =>
                      router.push(`/admin/dashboard/e/${employee.empid}`)
                    }
                  >
                    <span className="sr-only sm:not-sr-only sm:mr-2">
                      View Details
                    </span>
                    <ChevronRight className="h-4 w-4" />
                  </Button>
                </div>
              </Card>
            ))
          )}
        </div>
      </div>
    </main>
  );
}
