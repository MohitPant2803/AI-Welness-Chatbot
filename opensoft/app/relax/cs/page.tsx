/* eslint-disable @next/next/no-img-element */
"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Input } from "@/components/ui/input";
import { baseURL } from "@/lib/helperFunctions";
import {
  ArrowLeft,
  Search,
  Play,
  Waves,
  Trees,
  Music,
  Heart,
} from "lucide-react";
import Navbar from "@/components/navbar";

interface Sound {
  id: number;
  name: string;
  description: string;
  genre: string;
  url: string;
  thumbnailUrl: string;
  length: string;
  isPopular: boolean;
}

export default function CalmingSoundsPage() {
  const router = useRouter();
  const [searchQuery, setSearchQuery] = useState("");
  const [activeCategory, setActiveCategory] = useState("all");
  const [sounds, setSounds] = useState<Sound[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchSounds = async () => {
      try {
        const token = localStorage.getItem("token");
        if (!token) {
          router.push("/auth/signin");
          return;
        }

        const response = await fetch(`${baseURL}/a/api/v1/emp/details/sounds`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          throw new Error("Failed to fetch sounds");
        }

        const data = await response.json();
        setSounds(data.data.sounds);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to fetch sounds");
      } finally {
        setIsLoading(false);
      }
    };

    fetchSounds();
  }, [router]);

  // Filter sounds based on search query and active category
  const filteredSounds = sounds.filter((sound) => {
    const matchesSearch =
      sound.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      sound.description.toLowerCase().includes(searchQuery.toLowerCase());

    const matchesCategory =
      activeCategory === "all" ||
      (activeCategory === "popular" && sound.isPopular) ||
      activeCategory === sound.genre;

    return matchesSearch && matchesCategory;
  });

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        Loading...
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <Card className="p-4 text-red-500">
          Error: {error}
          <Button onClick={() => window.location.reload()} className="mt-2">
            Retry
          </Button>
        </Card>
      </div>
    );
  }
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 p-4 md:p-8">
      <Navbar />

      <div className="mx-auto max-w-7xl pt-16 md:pt-20">
        {/* Header Section */}
        <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex-1">
            <Button
              variant="ghost"
              onClick={() => router.push("/relax")}
              className="mb-2 -ml-2 flex items-center p-2 text-sm font-semibold sm:text-base"
            >
              <ArrowLeft className="mr-2 h-4 w-4" />
              <span className="hidden sm:inline">Back to Relax & Chill</span>
              <span className="sm:hidden">Back</span>
            </Button>
            <h2 className="text-xl font-bold text-gray-800 md:text-2xl lg:text-3xl">
              Calming Sounds
            </h2>
            <p className="mt-1 text-sm text-gray-600 md:text-base">
              Relax and unwind with our collection of soothing sounds
            </p>
          </div>

          {/* Search Input */}
          <div className="relative w-full sm:w-64">
            <Search className="absolute top-2.5 left-2.5 h-4 w-4 text-gray-500" />
            <Input
              type="search"
              placeholder="Search sounds..."
              className="w-full border-gray-200 bg-white pl-8 text-sm md:text-base"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
        </div>

        {/* Category Tabs */}
        <Tabs
          defaultValue="all"
          value={activeCategory}
          onValueChange={setActiveCategory}
          className="mb-6"
        >
          <TabsList className="mb-4 flex w-full overflow-x-auto rounded-md bg-gray-100 p-1 sm:min-w-max sm:flex-nowrap">
            {["all", "popular", "nature", "meditation", "music", "ambient"].map(
              (tab) => (
                <TabsTrigger
                  key={tab}
                  value={tab}
                  className="flex-shrink-0 rounded-md px-3 py-2 text-xs font-semibold text-gray-700 capitalize transition-colors data-[state=active]:bg-white data-[state=active]:text-black data-[state=active]:shadow sm:text-sm"
                >
                  {tab === "popular" ? "🔥 Popular" : tab}
                </TabsTrigger>
              )
            )}
          </TabsList>
        </Tabs>

        {/* Sound Grid */}
        {filteredSounds.length === 0 ? (
          <Card className="rounded-xl border border-gray-100 bg-white p-4 text-center shadow-sm md:p-8">
            <p className="text-sm text-gray-600 md:text-base">
              No sounds match your search criteria.
            </p>
            <Button
              variant="link"
              onClick={() => {
                setSearchQuery("");
                setActiveCategory("all");
              }}
              className="mt-2 text-sm md:text-base"
            >
              Clear filters
            </Button>
          </Card>
        ) : (
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 md:gap-6 lg:grid-cols-3 xl:grid-cols-4">
            {filteredSounds.map((sound) => (
              <Card
                key={sound.id}
                className="cursor-pointer overflow-hidden rounded-xl border border-gray-100 bg-white shadow-sm transition-transform duration-200 hover:-translate-y-1 hover:shadow-md"
                onClick={() => router.push(`/relax/cs/${sound.id}`)}
              >
                {/* Image Container */}
                <div className="relative aspect-square overflow-hidden bg-gray-100">
                  <img
                    src={sound.thumbnailUrl || "/placeholder.svg"}
                    alt={sound.name}
                    loading="lazy"
                    className="h-full w-full object-cover transition-transform duration-500 hover:scale-110"
                  />
                  <div className="absolute inset-0 flex items-center justify-center bg-black/20 opacity-0 transition-opacity hover:opacity-100">
                    <Button
                      size="icon"
                      variant="secondary"
                      className="h-10 w-10 rounded-full md:h-12 md:w-12"
                    >
                      <Play className="h-4 w-4 md:h-6 md:w-6" />
                    </Button>
                  </div>
                  {sound.isPopular && (
                    <Badge
                      className="absolute top-2 right-2 rounded-md bg-amber-100 px-2 py-1 text-xs font-bold text-amber-800"
                      variant="secondary"
                    >
                      Popular
                    </Badge>
                  )}
                </div>

                {/* Sound Info */}
                <div className="p-3 md:p-4">
                  <div className="mb-2 flex items-center gap-2">
                    <div className="flex-shrink-0 rounded-full bg-gray-100 p-1.5 md:p-2">
                      {getCategoryIcon(sound.genre)}
                    </div>
                    <div>
                      <h3 className="text-sm font-semibold text-gray-800 md:text-base">
                        {sound.name}
                      </h3>
                      <p className="text-xs text-gray-500 md:text-sm">
                        {sound.length}
                      </p>
                    </div>
                  </div>
                  <p className="line-clamp-2 text-xs text-gray-600 md:text-sm">
                    {sound.description}
                  </p>
                </div>
              </Card>
            ))}
          </div>
        )}
      </div>

      {/* Background Effects - Hidden on mobile */}
      <div className="animate-blob fixed top-20 left-10 hidden h-72 w-72 rounded-full bg-purple-200 opacity-30 mix-blend-multiply blur-3xl sm:block" />
      <div className="animate-blob animation-delay-2000 fixed top-40 right-10 hidden h-72 w-72 rounded-full bg-yellow-200 opacity-30 mix-blend-multiply blur-3xl sm:block" />
      <div className="animate-blob animation-delay-4000 fixed bottom-20 left-40 hidden h-72 w-72 rounded-full bg-pink-200 opacity-30 mix-blend-multiply blur-3xl sm:block" />
    </main>
  );
}

function getCategoryIcon(genre: string) {
  switch (genre.toLowerCase()) {
    case "nature":
      return <Trees className="h-6 w-6" />;
    case "meditation":
      return <Heart className="h-6 w-6" />;
    case "music":
      return <Music className="h-6 w-6" />;
    case "ambient":
      return <Waves className="h-6 w-6" />;
    default:
      return <Music className="h-6 w-6" />;
  }
}
