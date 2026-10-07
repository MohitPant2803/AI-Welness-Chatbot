/* eslint-disable @next/next/no-img-element */
/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import { useState, useRef, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Slider } from "@/components/ui/slider";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { baseURL } from "@/lib/helperFunctions";
import {
  Heart,
  Share2,
  Download,
  ArrowLeft,
  Play,
  Pause,
  SkipBack,
  SkipForward,
  Volume2,
  Volume1,
  VolumeX,
  Repeat,
  AlertCircle,
} from "lucide-react";
import Navbar from "@/components/navbar";

interface Sound {
  id: string;
  name: string;
  description: string;
  genre: string;
  url: string;
  thumbnailUrl: string;
  length: string;
  isPopular: boolean;
}

const formatTime = (seconds: number) => {
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${mins}:${secs < 10 ? "0" : ""}${secs}`;
};

const convertTimeToSeconds = (timeString: string) => {
  const [minutes, seconds] = timeString.split(":").map(Number);
  return minutes * 60 + seconds;
};

export default function SoundPlayerPage() {
  const router = useRouter();
  const { soundId } = useParams();
  const [currentSound, setCurrentSound] = useState<Sound | null>(null);
  const [relatedSounds, setRelatedSounds] = useState<Sound[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [volume, setVolume] = useState(80);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [isLooping, setIsLooping] = useState(false);
  const [isFavorite, setIsFavorite] = useState(false);
  const [showVolumeControls, setShowVolumeControls] = useState(false);
  const audioRef = useRef<HTMLAudioElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  // Audio visualization effect
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let animationId: number;
    const draw = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      const waveCount = 3;
      const waveColors = [
        "rgba(139, 92, 246, 0.5)",
        "rgba(139, 92, 246, 0.3)",
        "rgba(139, 92, 246, 0.1)",
      ];
      const baseHeight = canvas.height / 2;

      for (let i = 0; i < waveCount; i++) {
        const amplitude = isPlaying ? 20 - i * 5 : 5 - i;
        const frequency = 0.02;
        const speed = 0.05;
        const offset = Date.now() * speed * (i + 1) * 0.1;

        ctx.beginPath();
        ctx.moveTo(0, baseHeight);
        for (let x = 0; x < canvas.width; x++) {
          const y = baseHeight + Math.sin(x * frequency + offset) * amplitude;
          ctx.lineTo(x, y);
        }
        ctx.lineTo(canvas.width, canvas.height);
        ctx.lineTo(0, canvas.height);
        ctx.closePath();
        ctx.fillStyle = waveColors[i];
        ctx.fill();
      }
      animationId = requestAnimationFrame(draw);
    };

    draw();
    return () => cancelAnimationFrame(animationId);
  }, [isPlaying]);

  useEffect(() => {
    const fetchSoundData = async () => {
      try {
        const token = localStorage.getItem("token");
        if (!token) {
          router.push("/auth/signin");
          return;
        }

        const response = await fetch(`${baseURL}/a/api/v1/emp/details/sounds`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (!response.ok) throw new Error("Failed to fetch sounds");

        const { data } = await response.json();
        const sounds: Sound[] = data.sounds.map((s: any) => ({
          id: s.id,
          name: s.name,
          description: s.description,
          genre: s.genre,
          url: s.url,
          thumbnailUrl: s.thumbnailUrl,
          length: s.length,
          isPopular: s.isPopular,
        }));

        const foundSound = sounds.find(
          (s: Sound) => s.id.toString() === (soundId?.toString() ?? "")
        );
        if (!foundSound) throw new Error("Sound not found");

        setCurrentSound(foundSound);
        setRelatedSounds(
          sounds
            .filter((s) => s.id.toString() !== (soundId?.toString() ?? ""))
            .slice(0, 4)
        );
        setDuration(convertTimeToSeconds(foundSound.length));
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load sound");
      } finally {
        setIsLoading(false);
      }
    };

    fetchSoundData();
  }, [soundId, router]);

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio || !currentSound) return;

    const handleTimeUpdate = () => setCurrentTime(audio.currentTime);
    const handleEnded = () => setIsPlaying(false);

    audio.addEventListener("timeupdate", handleTimeUpdate);
    audio.addEventListener("ended", handleEnded);

    return () => {
      audio.removeEventListener("timeupdate", handleTimeUpdate);
      audio.removeEventListener("ended", handleEnded);
    };
  }, [currentSound]);

  // Handle window resize for responsive adjustments
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth >= 768) {
        setShowVolumeControls(true);
      }
    };

    // Set initial state based on window size
    handleResize();

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  const togglePlayPause = () => {
    const audio = audioRef.current;
    if (!audio) return;

    if (isPlaying) {
      audio.pause();
    } else {
      audio.play().catch(() => setIsPlaying(false));
    }
    setIsPlaying(!isPlaying);
  };

  const handleVolumeChange = (value: number[]) => {
    const newVolume = value[0];
    setVolume(newVolume);
    if (audioRef.current) audioRef.current.volume = newVolume / 100;
  };

  const handleSeek = (value: number[]) => {
    const newTime = value[0];
    setCurrentTime(newTime);
    if (audioRef.current) audioRef.current.currentTime = newTime;
  };

  const toggleVolumeControls = () => {
    setShowVolumeControls(!showVolumeControls);
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
        <Navbar />
        <div className="mx-auto max-w-7xl p-4 pt-20 sm:p-6 md:pt-24 lg:p-8">
          <Skeleton className="mb-6 h-8 w-32 sm:h-10 sm:w-40 md:mb-8 md:h-12 md:w-48" />
          <div className="grid grid-cols-1 gap-4 sm:gap-6 md:gap-8 lg:grid-cols-3 lg:gap-10">
            <Skeleton className="h-[400px] sm:h-[500px] md:h-[550px] lg:col-span-1 lg:h-[600px]" />
            <div className="space-y-6 sm:space-y-8 md:space-y-10 lg:col-span-2">
              <Skeleton className="h-[300px] sm:h-[350px] md:h-[400px]" />
              <Skeleton className="h-[200px] sm:h-[250px] md:h-[300px]" />
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error || !currentSound) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
        <Navbar />
        <div className="mx-auto max-w-7xl p-4 pt-20 sm:p-6 md:pt-24 lg:p-8">
          <Card className="p-6 text-center">
            <AlertCircle className="mx-auto mb-4 h-8 w-8 text-red-500 sm:h-10 sm:w-10 md:h-12 md:w-12" />
            <h2 className="mb-2 text-lg font-semibold text-red-600 sm:text-xl">
              {error ? "Error Loading Sound" : "Sound Not Found"}
            </h2>
            <Button
              onClick={() => router.push("/relax/cs")}
              className="mt-4 cursor-pointer"
            >
              Back to Calming Sounds
            </Button>
          </Card>
        </div>
      </div>
    );
  }

  const VolumeIcon = volume === 0 ? VolumeX : volume < 50 ? Volume1 : Volume2;

  return (
    <main className="relative min-h-screen overflow-hidden bg-gradient-to-br from-blue-50 to-purple-50 p-4 sm:p-6 md:p-8 lg:p-12">
      <Navbar />

      <div className="mx-auto max-w-7xl pt-20 sm:pt-16 md:pt-14">
        <Button
          variant="ghost"
          onClick={() => router.push("/relax/cs")}
          className="mb-4 cursor-pointer sm:mb-6 md:mb-8"
          size="sm"
        >
          <ArrowLeft className="mr-1 h-4 w-4 sm:mr-2 sm:h-5 sm:w-5" />
          <span className="text-sm sm:text-base">Back to Calming Sounds</span>
        </Button>

        <div className="grid grid-cols-1 gap-6 sm:gap-8 md:gap-10 lg:grid-cols-3">
          {/* Left Column - Sound Info */}
          <div className="lg:col-span-1">
            <Card className="overflow-hidden border-gray-200 bg-white">
              <div className="relative aspect-square w-full cursor-pointer">
                <img
                  src={currentSound.thumbnailUrl}
                  alt={currentSound.name}
                  className="h-full w-full rounded-t-lg object-cover"
                  onError={(e) => {
                    (e.target as HTMLImageElement).src =
                      "/placeholder-sound.jpg";
                  }}
                />
                {currentSound.isPopular && (
                  <Badge className="absolute top-2 right-2 bg-black text-xs font-semibold text-white">
                    Popular
                  </Badge>
                )}
              </div>
              <div className="p-3 sm:p-4 md:p-6">
                <h2 className="text-xl font-bold sm:text-2xl">
                  {currentSound.name}
                </h2>
                <Badge
                  variant="outline"
                  className="mt-1 border-gray-200 text-xs shadow sm:mt-2 sm:text-sm"
                >
                  {currentSound.genre}
                </Badge>
                <p className="mt-2 text-sm text-gray-600 sm:mt-4 sm:text-base">
                  {currentSound.description}
                </p>
                <div className="mt-4 flex items-center justify-between sm:mt-6">
                  <div className="flex gap-2 sm:gap-3">
                    <Button
                      variant="outline"
                      size="icon"
                      className="h-8 w-8 cursor-pointer border-gray-200 shadow sm:h-10 sm:w-10"
                      onClick={() => setIsFavorite(!isFavorite)}
                    >
                      <Heart
                        className={`h-4 w-4 sm:h-5 sm:w-5 ${isFavorite ? "text-red-500" : ""}`}
                      />
                    </Button>
                    <Button
                      variant="outline"
                      size="icon"
                      className="h-8 w-8 cursor-pointer border-gray-200 shadow sm:h-10 sm:w-10"
                    >
                      <Share2 className="h-4 w-4 sm:h-5 sm:w-5" />
                    </Button>
                    <Button
                      variant="outline"
                      size="icon"
                      className="h-8 w-8 cursor-pointer border-gray-200 shadow sm:h-10 sm:w-10"
                    >
                      <Download className="h-4 w-4 sm:h-5 sm:w-5" />
                    </Button>
                  </div>
                  <span className="text-xs text-gray-500 sm:text-sm">
                    {currentSound.length}
                  </span>
                </div>
              </div>
            </Card>
          </div>

          {/* Right Column - Player & Related */}
          <div className="space-y-6 sm:space-y-8 md:space-y-10 lg:col-span-2">
            {/* Player */}
            <Card className="border-gray-200 bg-white p-4 sm:p-6 md:p-8">
              <div className="space-y-4 sm:space-y-6">
                {/* Visualizer */}
                <div className="mb-4 flex items-center justify-center sm:mb-6 md:mb-8">
                  <div className="relative h-24 w-full max-w-3xl overflow-hidden rounded-xl bg-gray-100 sm:h-28 md:h-32">
                    <canvas
                      ref={canvasRef}
                      className="absolute inset-0 h-full w-full"
                      width={800}
                      height={128}
                    />
                  </div>
                </div>

                {/* Progress Bar */}
                <div className="space-y-1 sm:space-y-2">
                  <Slider
                    value={[currentTime]}
                    max={duration}
                    onValueChange={handleSeek}
                    className="[&>.slider-track]:bg-primary/20 [&>.slider-range]:bg-primary cursor-pointer"
                  />
                  <div className="flex justify-between text-xs text-gray-700 sm:text-sm">
                    <span>{formatTime(currentTime)}</span>
                    <span>{formatTime(duration)}</span>
                  </div>
                </div>

                {/* Controls */}
                <div className="flex flex-col items-center justify-between gap-4 sm:flex-row sm:gap-0">
                  {/* Playback Controls */}
                  <div className="flex items-center gap-2 sm:gap-4">
                    <Button
                      variant="ghost"
                      size="icon"
                      className="h-8 w-8 cursor-pointer sm:h-10 sm:w-10"
                    >
                      <SkipBack className="h-4 w-4 sm:h-5 sm:w-5" />
                    </Button>
                    <Button
                      size="icon"
                      className="bg-primary hover:bg-primary/90 h-12 w-12 cursor-pointer rounded-full sm:h-14 sm:w-14"
                      onClick={togglePlayPause}
                    >
                      {isPlaying ? (
                        <Pause className="h-5 w-5 sm:h-6 sm:w-6" />
                      ) : (
                        <Play className="h-5 w-5 sm:h-6 sm:w-6" />
                      )}
                    </Button>
                    <Button
                      variant="ghost"
                      size="icon"
                      className="h-8 w-8 cursor-pointer sm:h-10 sm:w-10"
                    >
                      <SkipForward className="h-4 w-4 sm:h-5 sm:w-5" />
                    </Button>
                  </div>

                  {/* Volume & Loop Controls */}
                  <div className="flex items-center gap-2 sm:gap-6">
                    <Button
                      variant={isLooping ? "default" : "ghost"}
                      size="icon"
                      className="h-8 w-8 cursor-pointer sm:h-10 sm:w-10"
                      onClick={() => setIsLooping(!isLooping)}
                    >
                      <Repeat className="h-4 w-4 sm:h-5 sm:w-5" />
                    </Button>

                    {/* Mobile volume toggle */}
                    <div className="sm:hidden">
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-8 w-8 cursor-pointer"
                        onClick={toggleVolumeControls}
                      >
                        <VolumeIcon className="h-4 w-4 text-gray-700" />
                      </Button>
                    </div>

                    {/* Volume slider - conditionally shown on mobile */}
                    <div
                      className={`flex items-center gap-2 ${showVolumeControls ? "flex" : "hidden sm:flex"}`}
                    >
                      <VolumeIcon className="hidden h-4 w-4 text-gray-700 sm:block sm:h-5 sm:w-5" />
                      <Slider
                        value={[volume]}
                        max={100}
                        onValueChange={handleVolumeChange}
                        className="w-24 cursor-pointer sm:w-32 [&>.slider-range]:bg-purple-600 [&>.slider-track]:bg-gray-200"
                      />
                    </div>
                  </div>
                </div>
              </div>
              <audio ref={audioRef} src={currentSound.url} loop={isLooping} />
            </Card>

            {/* Related Sounds */}
            <div>
              <h3 className="mb-3 text-xl font-bold text-gray-800 sm:mb-4 sm:text-2xl md:mb-6">
                You Might Also Like
              </h3>
              <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 sm:gap-4">
                {relatedSounds.map((sound) => (
                  <Card
                    key={sound.id}
                    className="hover:border-primary/30 group flex h-full cursor-pointer flex-row border-gray-200 bg-white p-2 transition-all hover:-translate-y-1 hover:shadow-lg sm:p-3"
                    onClick={() => router.push(`/relax/cs/${sound.id}`)}
                  >
                    {/* Thumbnail Container */}
                    <div className="relative h-16 w-16 flex-shrink-0 overflow-hidden rounded-lg sm:h-20 sm:w-24 md:h-24 md:w-32 md:rounded-xl">
                      <img
                        src={sound.thumbnailUrl}
                        alt={sound.name}
                        className="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
                        onError={(e) => {
                          (e.target as HTMLImageElement).src =
                            "/placeholder-sound.jpg";
                        }}
                      />
                    </div>

                    {/* Text Content */}
                    <div className="ml-2 flex min-w-0 flex-1 flex-col justify-between sm:ml-3 md:ml-4">
                      <div>
                        <h4 className="truncate text-sm font-bold text-gray-800 sm:text-base">
                          {sound.name}
                        </h4>
                        <Badge
                          variant="outline"
                          className="mt-1 bg-gray-100 text-xs text-gray-600"
                        >
                          {sound.genre}
                        </Badge>
                      </div>
                      <p className="mt-1 line-clamp-2 text-xs leading-tight text-gray-600 sm:mt-2 sm:text-sm">
                        {sound.description}
                      </p>
                    </div>
                  </Card>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
