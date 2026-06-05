"use client";

import {
  ConversationProvider,
  useConversationControls,
  useConversationStatus,
} from "@elevenlabs/react";
import { useState } from "react";

function VoiceAgent() {
  const { startSession, endSession } = useConversationControls();
  const { status } = useConversationStatus();
  const [error, setError] = useState("");

  const startVoice = async () => {
    try {
      setError("");

      await navigator.mediaDevices.getUserMedia({ audio: true });

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/voice/signed-url`
      );

      if (!response.ok) {
        throw new Error("Failed to get ElevenLabs signed URL");
      }

      const data = await response.json();

      await startSession({
        signedUrl: data.signed_url,
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Voice session failed");
    }
  };

  const stopVoice = async () => {
    await endSession();
  };

  return (
    <main className="min-h-screen bg-zinc-950 text-white flex items-center justify-center px-6">
      <section className="w-full max-w-xl border border-zinc-800 bg-zinc-900 p-6 rounded-lg">
        <h1 className="text-2xl font-semibold">DigitalTwinAI Voice</h1>

        <p className="mt-3 text-zinc-400">
          Talk with Abdul Samad Gilal&apos;s AI portfolio assistant.
        </p>

        <div className="mt-6 flex gap-3">
          <button
            onClick={startVoice}
            disabled={status === "connected"}
            className="rounded-md bg-cyan-500 px-4 py-2 font-medium text-zinc-950 disabled:opacity-50"
          >
            Start Voice
          </button>

          <button
            onClick={stopVoice}
            disabled={status !== "connected"}
            className="rounded-md border border-zinc-700 px-4 py-2 font-medium disabled:opacity-50"
          >
            End
          </button>
        </div>

        <p className="mt-4 text-sm text-zinc-400">Status: {status}</p>

        {error && <p className="mt-4 text-sm text-red-400">{error}</p>}
      </section>
    </main>
  );
}

export default function Home() {
  return (
    <ConversationProvider>
      <VoiceAgent />
    </ConversationProvider>
  );
}