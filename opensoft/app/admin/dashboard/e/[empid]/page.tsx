/* eslint-disable @next/next/no-img-element */
"use client";

import { use, useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Avatar } from "@/components/ui/avatar";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import {
  ArrowLeft,
  AlertTriangle,
  Clock,
  MessageSquare,
  Mail,
  Video,
  Heart,
  Award,
  Smile,
  TrendingUp,
  TrendingDown,
  Download,
  Loader2,
  Users,
} from "lucide-react";
import { baseURL, getMoodColor, getMoodIcon } from "@/lib/helperFunctions";
import AnimatedCounter from "@/components/AnimatedCounter";

interface BriefUserDetails {
  name: string;
  empid: string;
  dept: string;
  lastActive: string;
  currentMood: string;
  isEscalated: boolean;
  briefMoodSummary: string;
  avatarUrl: string;
  teamMessages: number;
  emailsSent: number;
  meetings: number;
  workHours: number;
}

interface MoodTrend {
  date: string;
  mood: string;
}

interface EarnedBadge {
  name: string;
  icon: string;
  description: string;
  slug: string;
}

interface CompanyAward {
  awardType: string;
  awardDate: string;
  rewardPoints: number;
}

interface LeaveRecord {
  leaveType: string;
  numberOfDays: number;
  startDate: string;
  endDate: string;
}

interface ChatRecord {
  message: string;
  timestamp: string;
  sender: string;
}

interface EmployeeDetailData {
  _id: string;
  briefUserDetails: BriefUserDetails;
  pastFiveMoodTrends: MoodTrend[];
  currentMoodRate: string;
  moodAnalysis: string;
  recommendedAction: string;
  earnedBadges: EarnedBadge[];
  companyAwards: CompanyAward[];
  leaveHistory: LeaveRecord[];
  chatHistory: ChatRecord[];
  chatAIAnalysis: string;
}

interface ApiResponse {
  success: boolean;
  message: string;
  data: EmployeeDetailData;
  code: number;
}

// Note the params prop is now a Promise that we unwrap using React.use()
export default function EmployeeDetailPage({
  params,
}: {
  params: Promise<{ empid: string }>;
}) {
  const resolvedParams = use(params);
  const { empid } = resolvedParams;
  const [isLoaded, setIsLoaded] = useState(false);
  const [isScheduling, setIsScheduling] = useState(false);

  const router = useRouter();
  const [employeeDetail, setEmployeeDetail] =
    useState<EmployeeDetailData | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const fetchEmployeeDetail = async () => {
    const token = localStorage.getItem("token");

    try {
      const res = await fetch(
        baseURL + `/a/api/v1/admin/details/db/emp/${empid}`,
        {
          method: "GET",
          headers: {
            Authorization: "Bearer " + token,
          },
        }
      );
      const json: ApiResponse = await res.json();
      if (!res.ok) {
        throw new Error(json.message || "Failed to fetch employee details");
      }
      setEmployeeDetail(json.data);

      // Add a slight delay to make the animation more noticeable
      setTimeout(() => {
        setIsLoaded(true);
      }, 300);
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchEmployeeDetail();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [empid]);

  const handleMeet = async () => {
    setIsScheduling(true);
    const token = localStorage.getItem("token");

    try {
      const res = await fetch(`${baseURL}/a/api/v1/admin/details/meet/${empid}`, {
        method: "POST",
        headers: {
          Authorization: "Bearer " + token,
        },
      });

      const result = await res.json();

      if (result.success) {
        const meetUrl = result.data;
        window.open(meetUrl, "_blank");
      } else {
        console.error("Error:", result.message);
      }
    } catch (error) {
      console.error("Error fetching meet URL:", error);
    } finally {
      setIsScheduling(false);
    }
  };

  if (isLoading || !employeeDetail) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-blue-50 to-purple-50">
        <Loader2 className="text-primary h-12 w-12 animate-spin" />
      </div>
    );
  }

  const details = employeeDetail.briefUserDetails;

  // Helper function to get mood bar width percentage
  const getMoodWidth = (mood: string) => {
    switch (mood) {
      case "Happy":
        return 100;
      case "TendingToHappy":
        return 80;
      case "Neutral":
        return 60;
      case "Sad":
        return 30;
      case "Angry":
        return 20;
      default:
        return 50;
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 pb-6">
      {/* Top Navigation Bar */}
      <nav className="fixed top-0 right-0 left-0 z-50 border-b border-gray-200 bg-white p-2 shadow-sm">
        <div className="mx-auto flex max-w-7xl flex-col items-center justify-between px-4 sm:flex-row">
          <div className="mb-2 flex w-full flex-col sm:mb-0 sm:w-auto">
            <div className="flex items-center gap-2">
              <Users className="h-5 w-5 text-black sm:h-6 sm:w-6" />
              <h1 className="text-lg font-bold text-black sm:text-xl">
                Admin Dashboard
              </h1>
            </div>
            <div
              onClick={() => router.push("/admin/dashboard")}
              className="flex w-full cursor-pointer items-center justify-start gap-2 text-xs text-gray-500 sm:justify-end sm:text-sm"
            >
              <ArrowLeft className="h-3 w-3 sm:h-4 sm:w-4" />
              <span>Back to Dashboard</span>
            </div>
          </div>
          <div className="flex w-full items-center justify-between gap-2 sm:w-auto sm:justify-end sm:gap-4">
            <Button
              variant="outline"
              size="sm"
              disabled={isScheduling}
              className="flex cursor-pointer items-center gap-1 border-gray-300 bg-blue-600 px-2 py-1 text-xs font-semibold text-white shadow-xs sm:gap-2 sm:px-3 sm:py-2 sm:text-sm"
              onClick={handleMeet}
            >
              <Video className="h-3 w-3 sm:h-4 sm:w-4" />
              <span className="xs:inline hidden">
                {isScheduling ? "Scheduling..." : "Schedule a Meet"}
              </span>
              <span className="xs:hidden inline">Meet</span>
            </Button>
            <a
              href={`${baseURL}/r/api/v1/get/report/${details.empid}`}
              target="_blank"
              rel="noopener noreferrer"
            >
              <Button
                variant="outline"
                size="sm"
                className="flex cursor-pointer items-center gap-1 border-gray-300 bg-white px-2 py-1 text-xs shadow-xs sm:gap-2 sm:px-3 sm:py-2 sm:text-sm"
              >
                <Download className="h-3 w-3 sm:h-4 sm:w-4" />
                <span>Export</span>
              </Button>
            </a>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => {
                localStorage.removeItem("token");
                router.push("/auth/signin");
              }}
              className="flex cursor-pointer items-center gap-1 px-2 py-1 text-xs font-bold sm:gap-2 sm:px-3 sm:py-2 sm:text-sm"
            >
              <ArrowLeft className="h-3 w-3 sm:h-4 sm:w-4" />
              <span className="xs:inline hidden">Sign Out</span>
              <span className="xs:hidden inline">Exit</span>
            </Button>
          </div>
        </div>
      </nav>

      <div className="mx-auto mt-6 max-w-7xl px-4 pt-24 sm:pt-20 md:px-8">
        {/* Employee Header */}
        <Card className="mb-6 w-full rounded-xl border border-gray-200 bg-white p-4 shadow-sm sm:p-6">
          <div className="flex flex-col items-center gap-4 sm:gap-6 md:flex-row md:items-start">
            {/* Avatar */}
            <Avatar className="h-20 w-20 rounded-xl border-4 border-white shadow-md sm:h-24 sm:w-24 md:h-32 md:w-32">
              <img
                src={details.avatarUrl || "/placeholder.svg"}
                alt={details.name}
              />
            </Avatar>

            {/* Info */}
            <div className="flex-grow text-center md:text-left">
              <div className="flex flex-col gap-2 md:flex-row md:items-center">
                <h2 className="text-xl font-bold text-gray-800 sm:text-2xl md:text-3xl">
                  {details.name}
                </h2>
                <Badge
                  className={`${getMoodColor(details.currentMood)} rounded-2xl text-xs font-semibold sm:text-sm md:ml-2`}
                >
                  {getMoodIcon(details.currentMood)}
                  <span className="ml-1">{details.currentMood}</span>
                </Badge>
              </div>
              <p className="text-sm text-gray-600 sm:text-base">
                ID: {details.empid}
              </p>

              {/* Stats */}
              <div className="mt-4 grid grid-cols-2 gap-3 sm:gap-4 md:grid-cols-4">
                <div className="flex flex-col items-center md:items-start">
                  <div className="mb-1 flex items-center text-gray-600">
                    <MessageSquare className="mr-1 h-3 w-3 sm:h-4 sm:w-4" />
                    <span className="text-xs sm:text-sm">Team Messages</span>
                  </div>
                  <span className="text-base font-semibold text-gray-800 sm:text-lg">
                    {isLoaded ? (
                      <AnimatedCounter
                        value={details.teamMessages}
                        duration={1500}
                      />
                    ) : (
                      0
                    )}
                  </span>
                </div>

                <div className="flex flex-col items-center md:items-start">
                  <div className="mb-1 flex items-center text-gray-600">
                    <Mail className="mr-1 h-3 w-3 sm:h-4 sm:w-4" />
                    <span className="text-xs sm:text-sm">Emails Sent</span>
                  </div>
                  <span className="text-base font-semibold text-gray-800 sm:text-lg">
                    {isLoaded ? (
                      <AnimatedCounter
                        value={details.emailsSent}
                        duration={1500}
                      />
                    ) : (
                      0
                    )}
                  </span>
                </div>

                <div className="flex flex-col items-center md:items-start">
                  <div className="mb-1 flex items-center text-gray-600">
                    <Video className="mr-1 h-3 w-3 sm:h-4 sm:w-4" />
                    <span className="text-xs sm:text-sm">Meetings</span>
                  </div>
                  <span className="text-base font-semibold text-gray-800 sm:text-lg">
                    {isLoaded ? (
                      <AnimatedCounter
                        value={details.meetings}
                        duration={1500}
                      />
                    ) : (
                      0
                    )}
                  </span>
                </div>

                <div className="flex flex-col items-center md:items-start">
                  <div className="mb-1 flex items-center text-gray-600">
                    <Clock className="mr-1 h-3 w-3 sm:h-4 sm:w-4" />
                    <span className="text-xs sm:text-sm">Work Hours</span>
                  </div>
                  <span className="text-base font-semibold text-gray-800 sm:text-lg">
                    {isLoaded ? (
                      <AnimatedCounter
                        value={details.workHours}
                        duration={1500}
                      />
                    ) : (
                      0
                    )}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </Card>

        {/* Tabs */}
        <Tabs defaultValue="mood" className="w-full">
          <TabsList className="mx-auto mb-4 grid w-full max-w-xs grid-cols-3 rounded-md bg-gray-100 p-1 sm:mb-6 sm:max-w-md">
            <TabsTrigger
              value="mood"
              className="flex cursor-pointer items-center justify-center gap-1 text-xs text-gray-700 data-[state=active]:bg-white data-[state=active]:font-semibold data-[state=active]:text-black sm:gap-2 sm:text-sm"
            >
              <Heart className="h-3 w-3 sm:h-4 sm:w-4" />
              <span>Mood</span>
            </TabsTrigger>
            <TabsTrigger
              value="achievements"
              className="flex cursor-pointer items-center justify-center gap-1 text-xs text-gray-700 data-[state=active]:bg-white data-[state=active]:font-semibold data-[state=active]:text-black sm:gap-2 sm:text-sm"
            >
              <Award className="h-3 w-3 sm:h-4 sm:w-4" />
              <span>Achievements</span>
            </TabsTrigger>
            <TabsTrigger
              value="chat"
              className="flex cursor-pointer items-center justify-center gap-1 text-xs text-gray-700 data-[state=active]:bg-white data-[state=active]:font-semibold data-[state=active]:text-black sm:gap-2 sm:text-sm"
            >
              <MessageSquare className="h-3 w-3 sm:h-4 sm:w-4" />
              <span>Chat</span>
            </TabsTrigger>
          </TabsList>

          {/* Mood History */}
          <TabsContent value="mood">
            <Card className="mb-6 rounded-xl border border-gray-200 bg-white p-4 shadow-sm sm:p-6">
              <h3 className="mb-3 text-lg font-extrabold text-gray-800 sm:mb-4 sm:text-xl">
                Mood History
              </h3>
              <div className="space-y-4 sm:space-y-6">
                {/* Recent Trend */}
                <div className="flex items-center justify-between">
                  <h4 className="text-sm font-semibold text-gray-700 sm:text-base">
                    Recent Trend
                  </h4>
                  <Badge
                    variant="outline"
                    className={`${
                      details.currentMood === "Sad"
                        ? "bg-red-100 text-red-800"
                        : "bg-green-100 text-green-800"
                    } rounded-2xl border-transparent text-xs font-semibold`}
                  >
                    {details.currentMood === "Sad" ? (
                      <TrendingDown className="mr-1 h-3 w-3" />
                    ) : (
                      <TrendingUp className="mr-1 h-3 w-3" />
                    )}
                    {details.currentMood === "Sad" ? "Declining" : "Improving"}
                  </Badge>
                </div>

                {/* Mood Graph */}
                <div className="rounded-lg bg-gray-50 p-3 sm:p-4">
                  <div className="flex flex-col space-y-3 sm:space-y-4">
                    {employeeDetail.pastFiveMoodTrends.map((item, index) => (
                      <div key={index} className="flex items-center">
                        <div className="w-8 text-xs text-gray-500 sm:w-12">
                          {new Date(item.date).toLocaleDateString("en-US", {
                            month: "short",
                            day: "numeric",
                          })}
                        </div>
                        <div className="w-20 sm:w-35">
                          <Badge
                            className={`${getMoodColor(item.mood)} rounded-2xl text-xs font-semibold`}
                          >
                            {getMoodIcon(item.mood)}
                            <span className="ml-1">{item.mood}</span>
                          </Badge>
                        </div>
                        <div className="ml-2 flex-grow sm:ml-4">
                          <div className="h-2 rounded-full bg-gray-200">
                            {isLoaded ? (
                              <div
                                className={`h-2 rounded-full transition-all duration-1000 ease-out ${
                                  item.mood === "Happy"
                                    ? "bg-green-500"
                                    : item.mood === "Neutral"
                                      ? "bg-gray-400"
                                      : item.mood === "Sad"
                                        ? "bg-red-500"
                                        : item.mood === "Angry"
                                          ? "bg-red-600"
                                          : "bg-lime-500"
                                }`}
                                style={{
                                  width: `${getMoodWidth(item.mood)}%`,
                                  transition: `width ${1200}ms ${index * 150}ms ease-out`,
                                }}
                              ></div>
                            ) : (
                              <div
                                className={`h-2 rounded-full ${
                                  item.mood === "Happy"
                                    ? "bg-green-500"
                                    : item.mood === "Neutral"
                                      ? "bg-gray-400"
                                      : item.mood === "Sad"
                                        ? "bg-red-500"
                                        : item.mood === "Angry"
                                          ? "bg-red-600"
                                          : "bg-lime-500"
                                }`}
                                style={{ width: "0%" }}
                              ></div>
                            )}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Mood Analysis */}
                <div>
                  <h4 className="mb-2 text-sm font-semibold text-gray-700 sm:text-base">
                    Mood Analysis
                  </h4>
                  <p className="mb-3 text-xs text-gray-600 sm:mb-4 sm:text-sm">
                    {employeeDetail.moodAnalysis}
                  </p>
                  <div className="rounded-lg border border-amber-200 bg-amber-50 p-3 sm:p-4">
                    <div className="flex items-start gap-2 sm:gap-3">
                      <AlertTriangle className="mt-0.5 h-4 w-4 text-amber-500 sm:h-5 sm:w-5" />
                      <div>
                        <h5 className="text-sm font-medium text-amber-800 sm:text-base">
                          Recommended Action
                        </h5>
                        <p className="mt-1 text-xs text-gray-600 sm:text-sm">
                          {employeeDetail.recommendedAction}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </Card>
          </TabsContent>

          {/* Achievements */}
          <TabsContent value="achievements">
            <div className="grid grid-cols-1 gap-4 sm:gap-6 md:grid-cols-2">
              {/* Earned Badges */}
              <Card className="rounded-xl border border-gray-200 bg-white p-4 shadow-sm sm:p-6">
                <h3 className="mb-3 text-lg font-bold text-gray-800 sm:mb-4 sm:text-xl">
                  Earned Badges
                </h3>
                <div className="space-y-3 sm:space-y-4">
                  {employeeDetail.earnedBadges.map((badge, index) => (
                    <div
                      key={index}
                      className="flex items-center gap-3 rounded-lg bg-gray-50 p-2 sm:gap-4 sm:p-3"
                    >
                      <div className="rounded-full bg-gray-200 p-2 text-xl sm:p-3 sm:text-2xl">
                        {badge.icon}
                      </div>
                      <div>
                        <h4 className="text-sm font-semibold text-gray-800 sm:text-base">
                          {badge.name}
                        </h4>
                        <p className="text-xs text-gray-500 sm:text-sm">
                          {badge.description}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </Card>

              {/* Company Awards */}
              <Card className="rounded-xl border border-gray-200 bg-white p-4 shadow-sm sm:p-6">
                <h3 className="mb-3 text-lg font-bold text-gray-800 sm:mb-4 sm:text-xl">
                  Company Awards
                </h3>
                <div className="space-y-3 sm:space-y-4">
                  {employeeDetail.companyAwards.map((award, index) => (
                    <div
                      key={index}
                      className="rounded-lg border border-amber-200 bg-gradient-to-br from-amber-50 to-amber-100 p-3 sm:p-4"
                    >
                      <div className="mb-2 flex items-start justify-between sm:mb-3">
                        <div className="rounded-full bg-amber-200 p-1 sm:p-2">
                          <Award className="h-4 w-4 text-amber-700 sm:h-5 sm:w-5" />
                        </div>
                        <span className="text-xs text-amber-700">
                          {new Date(award.awardDate).toLocaleDateString(
                            "en-US",
                            {
                              month: "long",
                              year: "numeric",
                            }
                          )}
                        </span>
                      </div>
                      <h4 className="text-sm font-semibold text-amber-800 sm:text-base">
                        {award.awardType}
                      </h4>
                      <p className="mt-1 text-xs text-amber-700 sm:text-sm">
                        +{award.rewardPoints} reward points
                      </p>
                    </div>
                  ))}
                </div>
              </Card>

              {/* Leave History */}
              <Card className="rounded-xl border border-gray-200 bg-white p-4 shadow-sm sm:p-6 md:col-span-2">
                <h3 className="mb-3 text-lg font-bold text-gray-800 sm:mb-4 sm:text-xl">
                  Leave History
                </h3>
                <div className="-mx-4 overflow-x-auto sm:mx-0">
                  <table className="w-full text-xs sm:text-sm">
                    <thead>
                      <tr className="border-b border-gray-200">
                        <th className="px-4 py-2 text-left font-semibold whitespace-nowrap text-gray-600 sm:py-3">
                          Type
                        </th>
                        <th className="px-4 py-2 text-left font-semibold whitespace-nowrap text-gray-600 sm:py-3">
                          Duration
                        </th>
                        <th className="px-4 py-2 text-left font-semibold whitespace-nowrap text-gray-600 sm:py-3">
                          Start Date
                        </th>
                        <th className="px-4 py-2 text-left font-semibold whitespace-nowrap text-gray-600 sm:py-3">
                          End Date
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      {employeeDetail.leaveHistory.map((leave, index) => (
                        <tr key={index} className="border-b border-gray-200">
                          <td className="px-4 py-2 whitespace-nowrap sm:py-3">
                            {leave.leaveType}
                          </td>
                          <td className="px-4 py-2 whitespace-nowrap sm:py-3">
                            {leave.numberOfDays} days
                          </td>
                          <td className="px-4 py-2 whitespace-nowrap sm:py-3">
                            {new Date(leave.startDate).toLocaleDateString()}
                          </td>
                          <td className="px-4 py-2 whitespace-nowrap sm:py-3">
                            {new Date(leave.endDate).toLocaleDateString()}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </Card>
            </div>
          </TabsContent>

          {/* Chat History */}
          <TabsContent value="chat">
            <Card className="rounded-xl border border-gray-200 bg-white p-4 shadow-sm sm:p-6">
              <h3 className="mb-3 text-lg font-extrabold text-gray-800 sm:mb-4 sm:text-xl">
                Chat History with Mindi (AI Assistant)
              </h3>
              <div
                className="chat-container mb-3 max-h-72 space-y-3 overflow-y-auto pr-2 sm:mb-4 sm:max-h-96 sm:space-y-4"
                style={{ scrollbarWidth: "thin" }}
                ref={(el) => {
                  if (el) {
                    // Scroll to bottom when the component mounts
                    el.scrollTop = el.scrollHeight;
                  }
                }}
              >
                {employeeDetail.chatHistory.map((chat, index) => {
                  // Check if sender is "user" to match with the employee
                  const isEmployee = chat.sender === "user";

                  return (
                    <div
                      key={index}
                      className={`flex ${isEmployee ? "justify-end" : "justify-start"}`}
                    >
                      {!isEmployee && (
                        <Avatar className="mr-2 h-6 w-6 bg-gray-200 sm:h-8 sm:w-8">
                          <Smile className="h-4 w-4 text-gray-700 sm:h-5 sm:w-5" />
                        </Avatar>
                      )}
                      <div
                        className={`max-w-[85%] rounded-2xl px-3 py-2 text-xs sm:px-4 sm:py-2 sm:text-sm ${
                          isEmployee
                            ? "bg-black text-white"
                            : "bg-gray-100 text-gray-800"
                        }`}
                      >
                        <p>{chat.message}</p>
                        <p className="mt-1 text-xs opacity-70">
                          {new Date(chat.timestamp).toLocaleTimeString([], {
                            hour: "2-digit",
                            minute: "2-digit",
                          })}
                        </p>
                      </div>
                      {isEmployee && (
                        <Avatar className="ml-2 h-6 w-6 bg-gray-200 sm:h-8 sm:w-8">
                          <img
                            src={details.avatarUrl || "/placeholder.svg"}
                            alt={details.name}
                          />
                        </Avatar>
                      )}
                    </div>
                  );
                })}
              </div>
              <div className="mt-4 rounded-lg border border-amber-200 bg-amber-50 p-3 sm:mt-6 sm:p-4">
                <div className="flex items-start gap-2 sm:gap-3">
                  <AlertTriangle className="mt-0.5 h-4 w-4 text-amber-500 sm:h-5 sm:w-5" />
                  <div>
                    <h5 className="text-sm font-medium text-amber-800 sm:text-base">
                      AI Analysis
                    </h5>
                    <p className="mt-1 text-xs text-gray-600 sm:text-sm">
                      {employeeDetail.chatAIAnalysis}
                    </p>
                  </div>
                </div>
              </div>
            </Card>
          </TabsContent>
        </Tabs>
      </div>

      {/* Decorative background elements */}
      <div className="animate-blob fixed -top-24 -left-24 h-48 w-48 rounded-full bg-purple-200 opacity-30 mix-blend-multiply blur-3xl sm:top-20 sm:left-10 sm:h-72 sm:w-72" />
      <div className="animate-blob animation-delay-2000 fixed -top-24 -right-24 h-48 w-48 rounded-full bg-yellow-200 opacity-30 mix-blend-multiply blur-3xl sm:top-40 sm:right-10 sm:h-72 sm:w-72" />
      <div className="animate-blob animation-delay-4000 fixed -bottom-24 left-1/4 h-48 w-48 rounded-full bg-pink-200 opacity-30 mix-blend-multiply blur-3xl sm:bottom-20 sm:left-40 sm:h-72 sm:w-72" />
    </main>
  );
}
