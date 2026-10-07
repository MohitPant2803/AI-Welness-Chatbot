"use client";

import { Loader2 } from "lucide-react";

export default function Loading() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-blue-50 to-purple-50">
      <Loader2 className="text-primary h-12 w-12 animate-spin" />
    </div>
  );
}
