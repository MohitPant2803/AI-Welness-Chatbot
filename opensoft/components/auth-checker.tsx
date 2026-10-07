// components/auth-checker.tsx
"use client";

import { useEffect } from "react";
import { usePathname, useRouter } from "next/navigation";
import { baseURL } from "@/lib/helperFunctions";

export default function AuthChecker() {
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem("token");

      // Immediately redirect if no token exists
      if (!token) {
        router.push("/auth/signin");
        return;
      }

      try {
        if (pathname === "/auth/signin") {
          return; // No need to check auth on the sign-in page
        }

        let url;
        if (pathname.startsWith("/admin")) {
          url = `${baseURL}/a/api/v1/admin/details/db`;
        } else {
          url = `${baseURL}/a/api/v1/emp/details/user`;
        }
        const res = await fetch(url, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!res.ok) {
          if (res.status === 401) {
            // Clear invalid token
            localStorage.removeItem("token");
            router.push("/auth/signin");
          }
          return;
        }
      } catch (error) {
        console.error("Auth check failed:", error);
        // Handle network errors or other exceptions
        localStorage.removeItem("token");
        router.push("/auth/signin");
      }
    };

    // Check auth on initial load and every route change
    checkAuth();
  }, [pathname, router]); // Add pathname and router as dependencies

  return null;
}
