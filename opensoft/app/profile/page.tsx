/* eslint-disable @next/next/no-img-element */
/* eslint-disable react-hooks/exhaustive-deps */
/* eslint-disable @typescript-eslint/no-unused-vars */
"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Avatar } from "@/components/ui/avatar";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { Calendar, Star, CheckCircle, Medal, Gift, Check } from "lucide-react";
import { baseURL } from "@/lib/helperFunctions";
import { MoodCalendar } from "@/components/MoodCalender";
import AnimatedProgressBar from "@/components/AnimatedProgressBar";
import { toast } from "sonner";
import { Toaster } from "@/components/ui/sonner";
import { motion, AnimatePresence } from "framer-motion";

// Custom SVG icon for Users
const UsersIcon = (props: React.SVGProps<SVGSVGElement>) => (
  <svg
    {...props}
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" />
    <circle cx="9" cy="7" r="4" />
    <path d="M22 21v-2a4 4 0 0 0-3-3.87" />
    <path d="M16 3.13a4 4 0 0 1 0 7.75" />
  </svg>
);

interface UserDetails {
  empid: string;
  name: string;
  streakDays: number;
  wellnessScore: number;
  numberOfteamMessages: number;
  numberOfemailsSent: number;
  dept: string;
  role: string;
  joinedOn: string;
  level: number;
  levelProgress: number;
  moodCalendar: { moodLevel: number; timestamp: string }[];
  recentTrends: {
    improvingTrend: { title: string; description: string; icon: string };
    consistentCheckIns: { title: string; description: string; icon: string };
    wellnessScore: { title: string; description: string; icon: string };
  };
  numberOfmeetingsAttended: number;
  workHours: number;
  currentVibe: string;
  vibeHistory: { moodLevel: number; timestamp: string }[];
  earnedBadges: {
    name: string;
    icon: string;
    description: string;
    slug: string;
  }[];
  badgesToUnlock: {
    name: string;
    icon: string;
    description: string;
    slug: string;
  }[];
  wellnessPoints: number;
  changedThisWeek: number;
  wellnessPointEntry: {
    chatCheckIn: { points: number; description: string };
    wellnessActivities: { points: number; description: string };
    streakBonus: { points: number; description: string };
  };
  avaiableRewards: {
    icon: string;
    name: string;
    pointsRequired: number;
    redeemedOn: string | null;
    id: string;
  }[];
  pastRewards: {
    icon: string;
    name: string;
    pointsRequired: number;
    redeemedOn: string;
    id: string;
  }[];
  avatar: string;
  leaves: {
    leaveType: string;
    numberOfDays: number;
    startDate: string;
    endDate: string;
  }[];
  awards: {
    awardType: string;
    awardDate: string;
    rewardPoints: number;
  }[];
  companyAwards: {
    title: string;
    dateReceived: string;
    description: string;
  }[];
}

interface ProfileApiResponse {
  success: boolean;
  message: string;
  data: {
    userDetails: UserDetails;
  };
  code: number;
}

export default function ProfilePage() {
  const [profile, setProfile] = useState<UserDetails | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isLoaded, setIsLoaded] = useState(false);
  const [redeemingReward, setRedeemingReward] = useState<string | null>(null);
  const [justRedeemedReward, setJustRedeemedReward] = useState<string | null>(
    null
  );
  const router = useRouter();

  // Fetch profile data from the API
  const fetchProfile = async () => {
    const token = localStorage.getItem("token");
    try {
      const res = await fetch(baseURL + "/a/api/v1/emp/details/user", {
        method: "GET",
        headers: {
          Authorization: "Bearer " + token,
        },
      });
      const json: ProfileApiResponse = await res.json();
      if (!res.ok) {
        // If token expired or unauthorized, redirect to signin
        if (res.status === 401) {
          router.push("/auth/signin");
          return;
        }
        throw new Error(json.message || "Failed to fetch profile");
      }

      // Add unique IDs to rewards if they don't have them
      const userDetails = json.data.userDetails;
      if (userDetails.avaiableRewards) {
        userDetails.avaiableRewards = userDetails.avaiableRewards.map(
          (reward, index) => ({
            ...reward,
            id:
              reward.id ||
              `available-${index}-${reward.name.replace(/\s+/g, "-").toLowerCase()}`,
          })
        );
      }

      if (userDetails.pastRewards) {
        userDetails.pastRewards = userDetails.pastRewards.map(
          (reward, index) => ({
            ...reward,
            id:
              reward.id ||
              `past-${index}-${reward.name.replace(/\s+/g, "-").toLowerCase()}`,
          })
        );
      }

      setProfile(userDetails);
      // Add a slight delay before animation starts for better visual effect
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
    fetchProfile();
  }, []);

  // Function to handle redeeming a reward
  const handleRedeemReward = async (reward: {
    name: string;
    pointsRequired: number;
    icon: string;
    id: string;
  }) => {
    if (!profile) return;

    // Check if user has enough points
    if (profile.wellnessPoints < reward.pointsRequired) {
      toast.error(
        `Not enough points! You need ${reward.pointsRequired - profile.wellnessPoints} more points.`,
        {
          className: "bg-opacity-100 font-medium", // Make toaster less transparent
        }
      );
      return;
    }

    // Set redeeming state to show animation
    setRedeemingReward(reward.id);

    try {
      // In a real app, this would be an API call to redeem the reward
      // For demo purposes, we're just updating the local state
      // await fetch(baseURL + `/api/v1/emp/redeem-reward/${reward.id}`, {...})

      // Simulate API delay
      await new Promise((resolve) => setTimeout(resolve, 1500));

      // Update the profile state
      setProfile((prevProfile) => {
        if (!prevProfile) return null;

        // Move the reward from available to past rewards
        const updatedAvailable = prevProfile.avaiableRewards.filter(
          (r) => r.id !== reward.id
        );

        const currentDate = new Date().toISOString();

        const updatedPastRewards = [
          ...prevProfile.pastRewards,
          {
            ...reward,
            redeemedOn: currentDate,
          },
        ];

        // Deduct points
        const updatedPoints =
          prevProfile.wellnessPoints - reward.pointsRequired;

        return {
          ...prevProfile,
          wellnessPoints: updatedPoints,
          avaiableRewards: updatedAvailable,
          pastRewards: updatedPastRewards,
        };
      });

      // Set just redeemed to trigger success animation
      setJustRedeemedReward(reward.id);

      // Show success toast with sonner
      toast.success(`Reward Redeemed!`, {
        description: `You've successfully redeemed ${reward.name} for ${reward.pointsRequired} points.`,
        icon: <Gift className="h-4 w-4" />,
        className: "bg-opacity-100 font-medium", // Make toaster less transparent
      });

      // Clear the redeemed state after animation
      setTimeout(() => {
        setRedeemingReward(null);
        setJustRedeemedReward(null);
      }, 2000);
    } catch (error) {
      console.error("Failed to redeem reward:", error);
      setRedeemingReward(null);

      toast.error("Redemption failed. Please try again.", {
        className: "bg-opacity-100 font-medium", // Make toaster less transparent
      });
    }
  };

  if (isLoading || !profile) {
    return (
      <div className="flex h-screen w-full items-center justify-center">
        <div className="animate-pulse text-xl font-medium">Loading...</div>
      </div>
    );
  }

  return (
    <main className="relative min-h-screen overflow-hidden bg-gradient-to-br from-blue-50 to-purple-50 p-2 sm:p-4 md:p-8">
      {/* Toaster component for notifications - Custom styling for less transparency */}
      <Toaster
        toastOptions={{
          className: "bg-opacity-100 border-0 shadow-lg", // Apply to all toasts
        }}
      />

      <div className="relative z-10 mx-auto max-w-7xl pt-12 sm:pt-16 md:pt-20 2xl:min-w-[75vw]">
        {/* Profile Header */}
        <Card className="mb-4 w-full rounded-xl border border-gray-100 bg-white shadow-lg sm:mb-6">
          <div className="flex flex-col items-center gap-4 p-4 sm:gap-6 sm:p-6 md:flex-row md:items-start md:p-8">
            {/* Avatar - Responsive sizing */}
            <Avatar className="h-20 w-20 rounded-xl border-4 border-white shadow-md sm:h-24 sm:w-24 md:h-32 md:w-32">
              <img
                src={profile.avatar || "/placeholder.svg"}
                alt={profile.name}
                className="object-cover"
              />
            </Avatar>

            {/* Info */}
            <div className="flex-grow text-center md:text-left">
              <h2 className="text-xl font-bold text-gray-800 sm:text-2xl md:text-3xl lg:text-4xl">
                {profile.name}
              </h2>
              <p className="text-sm text-gray-600 sm:text-base">
                {profile.role} • {profile.dept}
              </p>
              <p className="mt-1 text-xs text-gray-500 sm:text-sm">
                Member since{" "}
                {new Date(profile.joinedOn).toLocaleDateString("en-US", {
                  month: "long",
                  year: "numeric",
                })}
              </p>

              {/* Streak & Level Badges - Responsive spacing */}
              <div className="mt-3 flex flex-wrap justify-center gap-2 sm:mt-4 md:justify-start">
                <Badge
                  variant="secondary"
                  className="flex items-center gap-1 rounded-2xl bg-gray-100 px-2 py-1 text-xs font-bold whitespace-nowrap sm:px-3 sm:text-sm"
                >
                  <CheckCircle className="h-4 w-4 sm:h-5 sm:w-5" />
                  <span>{profile.streakDays} day streak</span>
                </Badge>
                <Badge
                  variant="secondary"
                  className="flex items-center gap-1 rounded-2xl bg-gray-100 px-2 py-1 text-xs font-bold whitespace-nowrap sm:px-3 sm:text-sm"
                >
                  <Star className="h-4 w-4 sm:h-5 sm:w-5" />
                  <span>Level {profile.level}</span>
                </Badge>
              </div>

              {/* Progress Bar - Now Animated */}
              <div className="mt-3 w-full sm:mt-4">
                <div className="mb-1 flex justify-between text-xs text-gray-500 sm:text-sm">
                  <span>Progress to Level {profile.level + 1}</span>
                  <span>{profile.levelProgress}%</span>
                </div>
                {isLoaded ? (
                  <AnimatedProgressBar
                    targetWidth={profile.levelProgress}
                    duration={1500}
                    backgroundColor="bg-gray-200"
                    foregroundColor="bg-black"
                  />
                ) : (
                  <div className="h-2 w-full rounded-full bg-gray-200">
                    <div
                      className="h-2 rounded-full bg-black"
                      style={{ width: "0%" }}
                    />
                  </div>
                )}
              </div>
            </div>
          </div>
        </Card>

        {/* Tabs - Improved for mobile */}
        <Tabs defaultValue="wellbeing" className="w-full">
          <TabsList className="mx-auto mb-4 grid w-full max-w-md grid-cols-3 rounded-md bg-gray-100 p-1 sm:mb-6">
            <TabsTrigger
              value="wellbeing"
              className="flex cursor-pointer items-center justify-center gap-1 text-sm text-gray-700 data-[state=active]:bg-white data-[state=active]:font-semibold data-[state=active]:text-black sm:gap-2 sm:text-base md:text-lg"
            >
              <Calendar className="h-4 w-4 sm:h-5 sm:w-5" />
              <span className="hidden sm:inline">Well-being</span>
              <span className="inline sm:hidden">Well</span>
            </TabsTrigger>
            <TabsTrigger
              value="badges"
              className="flex cursor-pointer items-center justify-center gap-1 text-sm text-gray-700 data-[state=active]:bg-white data-[state=active]:font-semibold data-[state=active]:text-black sm:gap-2 sm:text-base md:text-lg"
            >
              <Medal className="h-4 w-4 sm:h-5 sm:w-5" />
              <span>Badges</span>
            </TabsTrigger>
            <TabsTrigger
              value="rewards"
              className="flex cursor-pointer items-center justify-center gap-1 text-sm text-gray-700 data-[state=active]:bg-white data-[state=active]:font-semibold data-[state=active]:text-black sm:gap-2 sm:text-base md:text-lg"
            >
              <Gift className="h-4 w-4 sm:h-5 sm:w-5" />
              <span>Rewards</span>
            </TabsTrigger>
          </TabsList>

          {/* Well-being Tab */}
          <TabsContent value="wellbeing">
            <Card className="rounded-xl border border-gray-100 bg-white shadow-lg">
              <div className="p-4 sm:p-6">
                <h3 className="mb-3 text-xl font-extrabold text-gray-800 sm:mb-4 sm:text-2xl">
                  Mental Well-being Calendar
                </h3>
                <p className="mb-4 text-sm text-gray-500 sm:mb-6 sm:text-base">
                  Track your daily mood and well-being check-ins over time. More
                  consistent check-ins help us provide better support.
                </p>

                {/* Calendar Visualization - Improved mobile scrolling */}
                <div className="overflow-x-auto pb-4">
                  <div className="min-w-max">
                    <div className="flex flex-col gap-2">
                      {/* Day Labels */}
                      <div className="mb-1 flex justify-end gap-2 text-xs text-gray-500 sm:text-sm">
                        <div className="text-center">Mon</div>
                        <div className="text-center">Wed</div>
                        <div className="text-center">Fri</div>
                      </div>

                      {/* Calendar Grid */}
                      <MoodCalendar moodCalendar={profile.moodCalendar} />

                      {/* Legend - Smaller on mobile */}
                      <div className="mt-3 flex items-center justify-end gap-1 sm:mt-4 sm:gap-2">
                        <span className="text-xs text-gray-500 sm:text-sm">
                          Mood level:
                        </span>
                        <div className="h-4 w-4 rounded-md bg-red-200 sm:h-6 sm:w-6" />
                        <div className="h-4 w-4 rounded-md bg-yellow-200 sm:h-6 sm:w-6" />
                        <div className="h-4 w-4 rounded-md bg-green-200 sm:h-6 sm:w-6" />
                        <div className="h-4 w-4 rounded-md bg-emerald-300 sm:h-6 sm:w-6" />
                        <div className="h-4 w-4 rounded-md bg-blue-200 sm:h-6 sm:w-6" />
                      </div>
                    </div>
                  </div>
                </div>

                {/* Recent Trends - Responsive grid */}
                <div className="mt-6 sm:mt-8">
                  <h4 className="mb-2 text-base font-semibold text-gray-800 sm:mb-3 sm:text-lg">
                    Recent Trends
                  </h4>
                  <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 sm:gap-4 md:grid-cols-3">
                    <Card className="border-gray-200 p-3 shadow-sm sm:p-4">
                      <div className="flex items-center gap-2 sm:gap-3">
                        <div className="rounded-full bg-green-100 p-2 sm:p-3">
                          <span className="text-xl sm:text-2xl">
                            {profile.recentTrends.improvingTrend.icon}
                          </span>
                        </div>
                        <div>
                          <h5 className="text-sm font-bold text-gray-800 sm:text-base">
                            {profile.recentTrends.improvingTrend.title}
                          </h5>
                          <p className="text-xs text-gray-500 sm:text-sm">
                            {profile.recentTrends.improvingTrend.description}
                          </p>
                        </div>
                      </div>
                    </Card>

                    <Card className="border-gray-200 p-3 shadow-sm sm:p-4">
                      <div className="flex items-center gap-2 sm:gap-3">
                        <div className="rounded-full bg-purple-100 p-2 sm:p-3">
                          <span className="text-xl sm:text-2xl">
                            {profile.recentTrends.consistentCheckIns.icon}
                          </span>
                        </div>
                        <div>
                          <h5 className="text-sm font-bold text-gray-800 sm:text-base">
                            {profile.recentTrends.consistentCheckIns.title}
                          </h5>
                          <p className="text-xs text-gray-500 sm:text-sm">
                            {
                              profile.recentTrends.consistentCheckIns
                                .description
                            }
                          </p>
                        </div>
                      </div>
                    </Card>

                    <Card className="border-gray-200 p-3 shadow-sm sm:col-span-2 sm:p-4 md:col-span-1">
                      <div className="flex items-center gap-2 sm:gap-3">
                        <div className="rounded-full bg-blue-100 p-2 sm:p-3">
                          <span className="text-xl sm:text-2xl">
                            {profile.recentTrends.wellnessScore.icon}
                          </span>
                        </div>
                        <div>
                          <h5 className="text-sm font-bold text-gray-800 sm:text-base">
                            {profile.recentTrends.wellnessScore.title}
                          </h5>
                          <p className="text-xs text-gray-500 sm:text-sm">
                            {profile.recentTrends.wellnessScore.description}
                          </p>
                        </div>
                      </div>
                    </Card>
                  </div>
                </div>
              </div>
            </Card>
          </TabsContent>

          {/* Badges Tab */}
          <TabsContent value="badges">
            <div className="grid grid-cols-1 gap-4 sm:gap-6 md:grid-cols-2">
              {/* Earned Badges */}
              <Card className="rounded-xl border border-gray-100 bg-white shadow-lg">
                <div className="p-4 sm:p-6">
                  <h3 className="mb-3 text-xl font-bold text-gray-800 sm:mb-4 sm:text-2xl">
                    Earned Badges
                  </h3>
                  <p className="mb-4 text-sm text-gray-500 sm:mb-6 sm:text-base">
                    Badges are awarded for consistent engagement with the
                    wellness platform.
                  </p>
                  <div className="space-y-3 sm:space-y-4">
                    {profile.earnedBadges.map((badge, index) => (
                      <div
                        key={`earned-${badge.slug}-${index}`}
                        className="flex items-center gap-3 rounded-lg bg-gray-50 p-2 sm:gap-4 sm:p-3"
                      >
                        <div className="rounded-full bg-gray-200 p-2 sm:p-3">
                          <span className="text-xl sm:text-2xl">
                            {badge.icon}
                          </span>
                        </div>
                        <div>
                          <h4 className="text-base font-semibold text-gray-800 sm:text-lg">
                            {badge.name}
                          </h4>
                          <p className="text-xs text-gray-500 sm:text-sm">
                            {badge.description}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </Card>

              {/* Badges to Unlock */}
              <Card className="rounded-xl border border-gray-100 bg-white shadow-lg">
                <div className="p-4 sm:p-6">
                  <h3 className="mb-3 text-xl font-bold text-gray-800 sm:mb-4 sm:text-2xl">
                    Badges to Unlock
                  </h3>
                  <p className="mb-4 text-sm text-gray-500 sm:mb-6 sm:text-base">
                    Continue your wellness journey to unlock these badges.
                  </p>
                  <div className="space-y-3 sm:space-y-4">
                    {profile.badgesToUnlock.map((badge, index) => (
                      <div
                        key={`unlock-${badge.slug}-${index}`}
                        className="flex items-center gap-3 rounded-lg bg-gray-50 p-2 sm:gap-4 sm:p-3"
                      >
                        <div className="rounded-full bg-gray-100 p-2 text-gray-600 sm:p-3">
                          <span className="text-xl sm:text-2xl">
                            {badge.icon}
                          </span>
                        </div>
                        <div>
                          <h4 className="text-base font-bold text-gray-600 sm:text-lg">
                            {badge.name}
                          </h4>
                          <p className="text-xs text-gray-500 sm:text-sm">
                            {badge.description}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </Card>
            </div>
          </TabsContent>

          {/* Rewards Tab */}
          <TabsContent value="rewards">
            <div className="grid grid-cols-1 gap-4 sm:gap-6 md:grid-cols-3">
              {/* Points Summary */}
              <Card className="rounded-xl border border-gray-100 bg-white shadow-lg">
                <div className="p-4 sm:p-6">
                  <h3 className="mb-3 text-xl font-extrabold text-gray-800 sm:mb-4 sm:text-2xl">
                    Wellness Points
                  </h3>
                  <div className="flex items-center justify-center">
                    <div className="relative">
                      <div className="flex h-24 w-24 items-center justify-center rounded-full bg-gray-200 sm:h-32 sm:w-32">
                        <div className="text-2xl font-extrabold text-black sm:text-3xl">
                          <AnimatePresence>
                            <motion.span
                              key={profile.wellnessPoints}
                              initial={{ opacity: 0, y: -20 }}
                              animate={{ opacity: 1, y: 0 }}
                              exit={{ opacity: 0, y: 20 }}
                              transition={{ duration: 0.3 }}
                            >
                              {profile.wellnessPoints}
                            </motion.span>
                          </AnimatePresence>
                        </div>
                      </div>
                      <div className="absolute -top-2 -right-2 rounded-full bg-black px-2 py-1 text-xs font-bold text-white sm:text-sm">
                        +{profile.changedThisWeek} this week
                      </div>
                    </div>
                  </div>
                  <div className="mt-4 space-y-2 text-sm text-gray-600 sm:mt-6 sm:space-y-3 sm:text-base">
                    <div className="flex justify-between">
                      <span className="text-xs sm:text-sm">
                        {profile.wellnessPointEntry.chatCheckIn.description}
                      </span>
                      <span className="text-xs font-bold text-black sm:text-sm">
                        +{profile.wellnessPointEntry.chatCheckIn.points} pts
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-xs sm:text-sm">
                        {
                          profile.wellnessPointEntry.wellnessActivities
                            .description
                        }
                      </span>
                      <span className="text-xs font-bold text-black sm:text-sm">
                        +{profile.wellnessPointEntry.wellnessActivities.points}{" "}
                        pts
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-xs sm:text-sm">
                        {profile.wellnessPointEntry.streakBonus.description}
                      </span>
                      <span className="text-xs font-bold text-black sm:text-sm">
                        +{profile.wellnessPointEntry.streakBonus.points} pts
                      </span>
                    </div>
                  </div>
                </div>
              </Card>

              {/* Available Rewards */}
              <Card className="rounded-xl border border-gray-100 bg-white shadow-lg md:col-span-2">
                <div className="p-4 sm:p-6">
                  <h3 className="mb-3 text-xl font-extrabold text-gray-800 sm:mb-4 sm:text-2xl">
                    Available Rewards
                  </h3>
                  <p className="mb-4 text-xs text-gray-600 sm:mb-6 sm:text-sm md:text-base">
                    Redeem your wellness points for these rewards.
                  </p>
                  <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 sm:gap-4">
                    <AnimatePresence>
                      {profile.avaiableRewards.map((reward) => (
                        <motion.div
                          key={reward.id}
                          layout
                          initial={{ opacity: 0, scale: 0.8 }}
                          animate={{ opacity: 1, scale: 1 }}
                          exit={{
                            opacity: 0,
                            scale: 0.8,
                            y: -50,
                            transition: { duration: 0.5 },
                          }}
                          transition={{ duration: 0.3 }}
                          className="relative flex items-center gap-2 overflow-hidden rounded-lg border border-gray-100 p-3 shadow-sm sm:gap-4 sm:p-4"
                        >
                          {/* Redeeming Overlay - Improved Animation */}
                          {redeemingReward === reward.id && (
                            <motion.div
                              className="bg-opacity-90 absolute inset-0 z-10 flex items-center justify-center bg-black"
                              initial={{ opacity: 0 }}
                              animate={{ opacity: 1 }}
                              exit={{ opacity: 0 }}
                            >
                              <div className="text-center text-white">
                                <motion.div
                                  initial={{ rotate: 0 }}
                                  animate={{ rotate: 360 }}
                                  transition={{
                                    duration: 1.5,
                                    ease: "linear",
                                    repeat: Infinity,
                                  }}
                                >
                                  <svg
                                    className="mx-auto mb-2 h-12 w-12"
                                    xmlns="http://www.w3.org/2000/svg"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                  >
                                    <circle
                                      className="opacity-25"
                                      cx="12"
                                      cy="12"
                                      r="10"
                                      stroke="currentColor"
                                      strokeWidth="4"
                                    ></circle>
                                    <path
                                      className="opacity-75"
                                      fill="currentColor"
                                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                                    ></path>
                                  </svg>
                                </motion.div>
                                <p className="text-lg font-bold">
                                  Redeeming...
                                </p>
                              </div>
                            </motion.div>
                          )}

                          {/* Success Animation - Enhanced */}
                          {justRedeemedReward === reward.id && (
                            <motion.div
                              className="absolute inset-0 z-10 flex items-center justify-center bg-green-500"
                              initial={{ opacity: 0, scale: 0.9 }}
                              animate={{ opacity: 1, scale: 1 }}
                              exit={{ opacity: 0 }}
                              transition={{ duration: 0.4 }}
                            >
                              <div className="text-center text-white">
                                <motion.div
                                  initial={{ scale: 0, opacity: 0 }}
                                  animate={{ scale: 1, opacity: 1 }}
                                  transition={{
                                    type: "spring",
                                    stiffness: 300,
                                    damping: 15,
                                  }}
                                >
                                  <Check className="mx-auto mb-2 h-16 w-16" />
                                </motion.div>
                                <motion.p
                                  className="text-xl font-bold"
                                  initial={{ y: 10, opacity: 0 }}
                                  animate={{ y: 0, opacity: 1 }}
                                  transition={{ delay: 0.2 }}
                                >
                                  Redeemed!
                                </motion.p>
                              </div>
                            </motion.div>
                          )}

                          <div className="rounded-full bg-gray-200 p-3">
                            <span className="text-2xl">{reward.icon}</span>
                          </div>
                          <div className="flex-grow">
                            <h4 className="text-lg font-semibold text-gray-800">
                              {reward.name}
                            </h4>
                            <p className="font-medium text-black">
                              {reward.pointsRequired} pts
                            </p>
                          </div>
                          <Button
                            size="lg"
                            className={`cursor-pointer font-bold ${
                              profile.wellnessPoints >= reward.pointsRequired
                                ? "bg-black text-white hover:bg-gray-800"
                                : "bg-gray-300 text-gray-600"
                            }`}
                            onClick={() => handleRedeemReward(reward)}
                            disabled={
                              profile.wellnessPoints < reward.pointsRequired ||
                              redeemingReward !== null
                            }
                          >
                            Redeem
                          </Button>
                        </motion.div>
                      ))}
                    </AnimatePresence>
                  </div>

                  {/* Past Redemptions */}
                  <div className="mt-8">
                    <h4 className="mb-3 text-xl font-bold text-black">
                      Past Redemptions
                    </h4>
                    <div className="space-y-4 rounded-lg p-4">
                      <AnimatePresence>
                        {profile.pastRewards.map((reward) => (
                          <motion.div
                            key={reward.id}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0 }}
                            transition={{ duration: 0.3 }}
                            className="flex items-center justify-between"
                          >
                            <div className="flex items-center gap-3">
                              <span className="text-2xl">{reward.icon}</span>
                              <div>
                                <h5 className="text-lg font-bold text-gray-900">
                                  {reward.name}
                                </h5>
                                <p className="text-sm text-gray-500">
                                  Redeemed on{" "}
                                  {new Date(
                                    reward.redeemedOn
                                  ).toLocaleDateString()}
                                </p>
                              </div>
                            </div>
                            <span className="text-gray-500">
                              {reward.pointsRequired} pts
                            </span>
                          </motion.div>
                        ))}
                      </AnimatePresence>
                    </div>
                  </div>
                </div>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </main>
  );
}
