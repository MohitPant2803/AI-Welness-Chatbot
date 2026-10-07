/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Eye, EyeOff, User, Shield, LogIn } from "lucide-react";
import { baseURL } from "@/lib/helperFunctions";

export default function SignIn() {
  const router = useRouter();
  const [employeeID, setEmployeeID] = useState("");
  const [employeePassword, setEmployeePassword] = useState("");
  const [adminID, setAdminID] = useState("");
  const [adminPassword, setAdminPassword] = useState("");
  const [showEmployeePassword, setShowEmployeePassword] = useState(false);
  const [showAdminPassword, setShowAdminPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleEmployeeSignIn = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const response = await fetch(baseURL + "/a/api/v1/emp/auth/signin", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          empid: employeeID,
          password: employeePassword,
        }),
      });

      if (!response.ok)
        throw new Error("Failed to sign in. Please check your credentials.");
      const data = await response.json();
      if (!data.data?.token) {
        throw new Error("Invalid token received from the server.");
      }
      localStorage.setItem("token", data.data.token);

      router.push("/profile");
    } catch (error: any) {
      alert(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAdminSignIn = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const response = await fetch(baseURL + "/a/api/v1/admin/auth/signin", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ adminid: adminID, password: adminPassword }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(
          errorData.message ||
            "Failed to sign in. Please check your credentials."
        );
      }

      const data = await response.json();
      if (!data.data?.token) {
        throw new Error("Invalid token received from the server.");
      }
      localStorage.setItem("token", data.data.token);
      router.push("/admin/dashboard");
    } catch (error: any) {
      alert(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="flex h-screen w-screen items-center justify-center p-4">
      <Card className="w-full max-w-md rounded-xl border border-gray-200 bg-white shadow-md">
        {/* Header */}
        <div className="border-b border-gray-200 p-6 text-center">
          <h1 className="text-2xl font-bold text-black">
            Mental Wellness Portal
          </h1>
          <p className="mt-1 text-sm text-gray-700">
            Sign in to access your wellness resources
          </p>
        </div>

        {/* Tabs for Employee/Admin switching */}
        <Tabs defaultValue="employee" className="w-full">
          <div className="px-6 pt-4">
            <TabsList className="grid w-full grid-cols-2 rounded-sm bg-gray-100">
              <TabsTrigger
                value="employee"
                className="flex cursor-pointer items-center justify-center gap-2 rounded-sm font-semibold data-[state=active]:bg-white data-[state=active]:text-black data-[state=inactive]:text-gray-700"
              >
                <User className="h-4 w-4" />
                <span>Employee</span>
              </TabsTrigger>
              <TabsTrigger
                value="admin"
                className="flex cursor-pointer items-center justify-center gap-2 rounded-sm font-semibold data-[state=active]:bg-white data-[state=active]:text-black data-[state=inactive]:text-gray-700"
              >
                <Shield className="h-4 w-4" />
                <span>Admin</span>
              </TabsTrigger>
            </TabsList>
          </div>

          {/* Employee Login Form */}
          <TabsContent value="employee" className="p-6 pt-4">
            <form onSubmit={handleEmployeeSignIn}>
              <div className="space-y-4">
                <div className="space-y-2">
                  <label
                    htmlFor="employee-id"
                    className="text-sm font-bold text-gray-700"
                  >
                    Employee ID
                  </label>
                  <Input
                    id="employee-id"
                    type="text"
                    placeholder="EMPXXXX"
                    value={employeeID}
                    onChange={(e) => setEmployeeID(e.target.value)}
                    required
                    className="mt-3 rounded-md border border-gray-200 px-3 py-2 transition-all focus:border-transparent focus:ring-2 focus:ring-gray-500 focus:outline-none"
                  />
                </div>

                <div className="space-y-2">
                  <label
                    htmlFor="employee-password"
                    className="text-sm font-bold text-gray-700"
                  >
                    Password
                  </label>
                  <div className="relative">
                    <Input
                      id="employee-password"
                      type={showEmployeePassword ? "text" : "password"}
                      placeholder="••••••••"
                      value={employeePassword}
                      onChange={(e) => setEmployeePassword(e.target.value)}
                      required
                      className="mt-3 rounded-md border border-gray-300 px-3 py-2 pr-10 transition-all focus:border-transparent focus:ring-2 focus:ring-gray-500 focus:outline-none"
                    />
                    <Button
                      type="button"
                      onClick={() =>
                        setShowEmployeePassword(!showEmployeePassword)
                      }
                      className="absolute top-1/2 right-3 -translate-y-1/2 cursor-pointer text-gray-500 hover:text-gray-700"
                    >
                      {showEmployeePassword ? (
                        <EyeOff className="h-4 w-4" />
                      ) : (
                        <Eye className="h-4 w-4" />
                      )}
                    </Button>
                  </div>
                </div>

                <div className="pt-2">
                  <Button
                    type="submit"
                    className="w-full cursor-pointer bg-black text-white hover:bg-gray-800"
                    disabled={isLoading}
                  >
                    {isLoading ? (
                      <div className="flex items-center gap-2">
                        <div className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
                        <span>Signing in...</span>
                      </div>
                    ) : (
                      <div className="flex items-center justify-center gap-2 font-semibold">
                        <LogIn className="h-4 w-4" />
                        <span>Sign In</span>
                      </div>
                    )}
                  </Button>
                </div>

                <div className="text-center text-sm text-gray-600">
                  <a href="#" className="hover:text-gray-900 hover:underline">
                    Forgot your password?
                  </a>
                </div>
              </div>
            </form>
          </TabsContent>

          {/* Admin Login Form */}
          <TabsContent value="admin" className="p-6 pt-4">
            <form onSubmit={handleAdminSignIn}>
              <div className="space-y-4">
                <div className="space-y-2">
                  <label
                    htmlFor="admin-id"
                    className="text-sm font-bold text-gray-700"
                  >
                    Admin ID
                  </label>
                  <Input
                    id="admin-id"
                    type="text"
                    placeholder="ADMXXXX"
                    value={adminID}
                    onChange={(e) => setAdminID(e.target.value)}
                    required
                    className="mt-3 rounded-md border border-gray-300 px-3 py-2 transition-all focus:border-transparent focus:ring-2 focus:ring-purple-500 focus:outline-none"
                  />
                </div>

                <div className="space-y-2">
                  <label
                    htmlFor="admin-password"
                    className="text-sm font-bold text-gray-700"
                  >
                    Password
                  </label>
                  <div className="relative">
                    <Input
                      id="admin-password"
                      type={showAdminPassword ? "text" : "password"}
                      placeholder="••••••••"
                      value={adminPassword}
                      onChange={(e) => setAdminPassword(e.target.value)}
                      required
                      className="mt-3 rounded-md border border-gray-300 px-3 py-2 pr-10 transition-all focus:border-transparent focus:ring-2 focus:ring-purple-500 focus:outline-none"
                    />
                    <Button
                      type="button"
                      onClick={() => setShowAdminPassword(!showAdminPassword)}
                      className="absolute top-1/2 right-3 -translate-y-1/2 cursor-pointer text-gray-500 hover:text-gray-700"
                    >
                      {showAdminPassword ? (
                        <EyeOff className="h-4 w-4" />
                      ) : (
                        <Eye className="h-4 w-4" />
                      )}
                    </Button>
                  </div>
                </div>

                <div className="pt-2">
                  <Button
                    type="submit"
                    className="w-full cursor-pointer bg-black text-white hover:bg-gray-800"
                    disabled={isLoading}
                  >
                    {isLoading ? (
                      <div className="flex items-center gap-2">
                        <div className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
                        <span>Signing in...</span>
                      </div>
                    ) : (
                      <div className="flex items-center justify-center gap-2 font-semibold">
                        <Shield className="h-4 w-4" />
                        <span>Admin Sign In</span>
                      </div>
                    )}
                  </Button>
                </div>

                <div className="text-center text-sm text-gray-600">
                  <a href="#" className="hover:text-gray-900 hover:underline">
                    Contact IT support
                  </a>
                </div>
              </div>
            </form>
          </TabsContent>
        </Tabs>

        {/* Footer Note */}
        <div className="p-6 pt-0 text-center text-sm text-gray-600">
          <p>Your mental health matters. This portal is a safe space.</p>
        </div>
      </Card>
    </main>
  );
}
