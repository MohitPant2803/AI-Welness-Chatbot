"use client";

import React, { useState } from "react";
import { useRouter, usePathname } from "next/navigation";
import {
  MessageSquare,
  Coffee,
  User,
  Heart,
  ArrowLeft,
  Menu,
  X,
} from "lucide-react";
import { Button } from "@/components/ui/button";

export default function Navbar() {
  const router = useRouter();
  const pathname = usePathname();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  // If the path starts with "/admin" or "/auth", do not render the navbar.
  if (pathname.startsWith("/admin") || pathname.startsWith("/auth")) {
    return null;
  }

  // Define dynamic branding based on the current path.
  const branding = {
    default: {
      icon: <MessageSquare className="h-6 w-6 text-black sm:h-7 sm:w-7" />,
      label: "Chat",
    },
    relax: {
      icon: <Coffee className="h-6 w-6 text-black sm:h-7 sm:w-7" />,
      label: "Relax & Chill Zone",
    },
    profile: {
      icon: <Heart className="h-6 w-6 text-black sm:h-7 sm:w-7" />,
      label: "Mental Wellness Portal",
    },
  };

  // Determine the current branding based on the pathname.
  const currentBrand = pathname.includes("relax")
    ? branding.relax
    : pathname === "/profile"
      ? branding.profile
      : branding.default;

  // Function to toggle mobile menu
  const toggleMobileMenu = () => {
    setMobileMenuOpen(!mobileMenuOpen);
  };

  return (
    <nav className="fixed top-0 right-0 left-0 z-50 border-b border-gray-200 bg-white shadow-sm">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-2 md:px-6 md:py-4 2xl:max-w-[75vw]">
        {/* Dynamic Logo Section */}
        <div
          className="flex cursor-pointer items-center gap-1 sm:gap-2"
          onClick={() => router.push(pathname)}
        >
          {currentBrand.icon}
          <h1 className="truncate text-lg font-bold text-black sm:text-xl md:text-2xl">
            {currentBrand.label}
          </h1>
        </div>

        {/* Mobile menu button */}
        <div className="md:hidden">
          <Button
            variant="ghost"
            size="sm"
            className="px-2"
            onClick={toggleMobileMenu}
          >
            {mobileMenuOpen ? (
              <X className="h-5 w-5" />
            ) : (
              <Menu className="h-5 w-5" />
            )}
          </Button>
        </div>

        {/* Desktop Navigation Links */}
        <div className="hidden items-center gap-2 md:flex lg:gap-4">
          <Button
            variant="ghost"
            className={`flex cursor-pointer items-center gap-1 rounded-md text-base transition-transform duration-150 hover:scale-105 ${
              pathname === "/"
                ? "border-gray-100 bg-white font-semibold text-black shadow-sm"
                : "bg-gray-100 text-gray-800"
            }`}
            onClick={() => router.push("/")}
          >
            <MessageSquare className="h-4 w-4 lg:h-5 lg:w-5" />
            <span className="hidden sm:inline">Chat</span>
          </Button>
          <Button
            variant="ghost"
            className={`flex cursor-pointer items-center gap-1 rounded-md text-base transition-transform duration-150 hover:scale-105 ${
              pathname.includes("relax")
                ? "border-gray-100 bg-white font-semibold text-black shadow-sm"
                : "bg-gray-100 text-gray-800"
            }`}
            onClick={() => router.push("/relax")}
          >
            <Coffee className="h-4 w-4 lg:h-5 lg:w-5" />
            <span className="hidden sm:inline">Relax &amp; Chill</span>
          </Button>
          <Button
            variant="ghost"
            className={`flex cursor-pointer items-center gap-1 rounded-md text-base transition-transform duration-150 hover:scale-105 ${
              pathname === "/profile"
                ? "border-gray-100 bg-white font-semibold text-black shadow-sm"
                : "bg-gray-100 text-gray-800"
            }`}
            onClick={() => router.push("/profile")}
          >
            <User className="h-4 w-4 lg:h-5 lg:w-5" />
            <span className="hidden sm:inline">Profile</span>
          </Button>
          <Button
            variant="ghost"
            size={"sm"}
            className="flex cursor-pointer items-center text-sm text-gray-800 lg:text-base"
            onClick={() => {
              localStorage.removeItem("token");
              router.push("/auth/signin");
            }}
          >
            <ArrowLeft className="h-4 w-4" />
            <span className="hidden sm:inline">Sign Out</span>
          </Button>
        </div>
      </div>

      {/* Mobile menu dropdown */}
      {mobileMenuOpen && (
        <div className="space-y-2 bg-white px-4 pb-4 shadow-lg md:hidden">
          <Button
            variant="ghost"
            className={`flex w-full cursor-pointer items-center justify-start gap-2 rounded-md text-base ${
              pathname === "/"
                ? "border-gray-100 bg-white font-semibold text-black shadow-sm"
                : "bg-gray-100 text-gray-800"
            }`}
            onClick={() => {
              router.push("/");
              setMobileMenuOpen(false);
            }}
          >
            <MessageSquare className="h-5 w-5" />
            <span>Chat</span>
          </Button>
          <Button
            variant="ghost"
            className={`flex w-full cursor-pointer items-center justify-start gap-2 rounded-md text-base ${
              pathname.includes("relax")
                ? "border-gray-100 bg-white font-semibold text-black shadow-sm"
                : "bg-gray-100 text-gray-800"
            }`}
            onClick={() => {
              router.push("/relax");
              setMobileMenuOpen(false);
            }}
          >
            <Coffee className="h-5 w-5" />
            <span>Relax &amp; Chill</span>
          </Button>
          <Button
            variant="ghost"
            className={`flex w-full cursor-pointer items-center justify-start gap-2 rounded-md text-base ${
              pathname === "/profile"
                ? "border-gray-100 bg-white font-semibold text-black shadow-sm"
                : "bg-gray-100 text-gray-800"
            }`}
            onClick={() => {
              router.push("/profile");
              setMobileMenuOpen(false);
            }}
          >
            <User className="h-5 w-5" />
            <span>Profile</span>
          </Button>
          <Button
            variant="ghost"
            className="flex w-full cursor-pointer items-center justify-start gap-2 text-base text-gray-800"
            onClick={() => {
              localStorage.removeItem("token");
              router.push("/auth/signin");
            }}
          >
            <ArrowLeft className="h-5 w-5" />
            <span>Sign Out</span>
          </Button>
        </div>
      )}
    </nav>
  );
}
