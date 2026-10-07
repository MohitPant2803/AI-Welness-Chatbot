"use client";

import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ArrowLeft } from "lucide-react";
import { useRouter } from "next/navigation";

export default function RelaxPage() {
  const router = useRouter();

  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-br from-blue-50 to-purple-50 p-4 pt-20 md:p-8">
      {/* Main Content */}
      <div className="mx-auto mt-4 max-w-7xl 2xl:min-w-[75vw]">
        {/* Intro Card */}
        <Card className="mb-6 w-full gap-2 overflow-hidden rounded-xl border border-gray-100 bg-white shadow-lg">
          <div className="flex flex-col items-center justify-center gap-4 p-4 md:p-8">
            <h2 className="mb-2 text-3xl font-extrabold text-gray-800 md:text-4xl">
              Relax & Chill Zone
            </h2>
            <p className="max-w-2xl text-center text-base text-gray-700 md:text-lg">
              This page will be built later. It will contain relaxation
              exercises, meditation guides, and calming activities to help you
              unwind.
            </p>
          </div>
          <div className="ml-4 md:ml-8">
            <Button
              onClick={() => router.push("/profile")}
              className="flex cursor-pointer items-center gap-2 bg-black font-bold text-white hover:bg-gray-800"
            >
              <ArrowLeft className="h-4 w-4" />
              <span className="text-sm md:text-base">Return to Profile</span>
            </Button>
          </div>
        </Card>

        {/* Feature Cards */}
        <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
          {/* Calming Sounds */}
          <Card className="overflow-hidden rounded-xl border border-gray-100 bg-white shadow-lg">
            <div className="flex flex-col gap-4 p-4 text-center md:p-6">
              <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-purple-100 md:h-16 md:w-16">
                {/* Icon */}
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="text-purple-600"
                  width="24"
                  height="24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <path d="M3 18v-6a9 9 0 0 1 18 0v6"></path>
                  <path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"></path>
                </svg>
              </div>
              <h3 className="mb-2 text-xl font-semibold md:text-2xl">
                Calming Sounds
              </h3>
              <p className="text-sm text-gray-500 md:text-base">
                Nature sounds and ambient music to help you relax.
              </p>
              <Button
                className="mx-auto mt-4 w-fit cursor-pointer border-gray-200 font-semibold duration-200 hover:bg-gray-200"
                variant="outline"
                onClick={() => router.push("/relax/cs")}
              >
                Explore Sounds
              </Button>
            </div>
          </Card>

          {/* Breathing Exercises */}
          <Card className="overflow-hidden rounded-xl border border-gray-100 bg-white shadow-lg">
            <div className="flex flex-col gap-4 p-4 text-center md:p-6">
              <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-green-100 md:h-16 md:w-16">
                {/* Icon */}
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="text-green-600"
                  width="24"
                  height="24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
                </svg>
              </div>
              <h3 className="mb-2 text-xl font-semibold md:text-2xl">
                Breathing Exercises
              </h3>
              <p className="text-sm text-gray-500 md:text-base">
                Simple breathing techniques to reduce stress and anxiety.
              </p>
              <p className="mt-4 text-sm text-purple-600">Coming soon</p>
            </div>
          </Card>

          {/* Meditation Sessions */}
          <Card className="overflow-hidden rounded-xl border border-gray-100 bg-white shadow-lg">
            <div className="flex flex-col gap-4 p-4 text-center md:p-6">
              <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-blue-100 md:h-16 md:w-16">
                {/* Icon */}
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="text-blue-600"
                  width="24"
                  height="24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
                  <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
                </svg>
              </div>
              <h3 className="mb-2 text-xl font-semibold md:text-2xl">
                Guided Meditation
              </h3>
              <p className="text-sm text-gray-500 md:text-base">
                Guided meditation sessions to help you relax and focus.
              </p>
              <p className="mt-4 text-sm text-purple-600">Coming soon</p>
            </div>
          </Card>
        </div>
      </div>
      {/* Decorative background elements */}
      <div className="animate-blob fixed top-20 left-10 h-72 w-72 rounded-full bg-purple-300 opacity-30 mix-blend-multiply blur-3xl filter"></div>
      <div className="animate-blob animation-delay-2000 fixed top-40 right-10 h-72 w-72 rounded-full bg-yellow-200 opacity-30 mix-blend-multiply blur-3xl filter"></div>
      <div className="animate-blob animation-delay-4000 fixed bottom-20 left-40 h-72 w-72 rounded-full bg-pink-300 opacity-30 mix-blend-multiply blur-3xl filter"></div>
    </main>
  );
}
