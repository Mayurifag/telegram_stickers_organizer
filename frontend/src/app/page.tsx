"use client";

import { useState, useEffect } from 'react';
import axios from 'axios';
import Link from 'next/link';

interface StickerPack {
  name: string;
  title: string;
  user_id: number;
}

export default function Home() {
  const [stickerPacks, setStickerPacks] = useState<StickerPack[]>([]);

  useEffect(() => {
    const fetchStickerPacks = async () => {
      const response = await axios.get('http://localhost:8000/api/stickerpacks');
      setStickerPacks(response.data);
    };
    fetchStickerPacks();
  }, []);

  return (
    <div className="container mx-auto px-4">
      <h1 className="text-3xl font-bold my-4">Sticker Packs</h1>
      <Link href="/manage-stickers" className="text-blue-500 hover:underline mb-4 inline-block">
        Manage Sticker Sets
      </Link>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {stickerPacks.map((pack) => (
          <Link href={`/stickerpack/${pack.name}`} key={pack.name}>
            <div className="border rounded-lg p-6 cursor-pointer hover:shadow-2xl transition-shadow transform hover:scale-105 bg-modal">
              <h2 className="text-lg font-semibold">{pack.title}</h2>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
