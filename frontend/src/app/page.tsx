"use client";

import { useState, useEffect } from 'react';
import axios from 'axios';
import Link from 'next/link';

interface StickerPack {
  set_name: string;
  title: string;
}

export default function Home() {
  const [stickerPacks, setStickerPacks] = useState<StickerPack[]>([]);
  const [loadedImages, setLoadedImages] = useState<string[]>([]);

  useEffect(() => {
    const fetchStickerPacks = async () => {
      const response = await axios.get('http://localhost:8000/api/stickerpacks');
      setStickerPacks(response.data);
    };
    fetchStickerPacks();
  }, []);

  useEffect(() => {
    const cachedImages = JSON.parse(localStorage.getItem('loadedImages') || '[]');
    setLoadedImages(cachedImages);
  }, []);

  const handleImageLoad = (src: string) => {
    if (!loadedImages.includes(src)) {
      setLoadedImages((prev) => [...prev, src]);
      localStorage.setItem('loadedImages', JSON.stringify([...loadedImages, src]));
    }
  };

  return (
    <div className="container mx-auto px-4">
      <h1 className="text-3xl font-bold my-4">Sticker Packs</h1>
      <Link href="/manage-stickers" className="text-blue-500 hover:underline mb-4 inline-block">
        Manage Sticker Sets
      </Link>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {stickerPacks.map((pack) => (
          <Link href={`/stickerpack/${pack.set_name}`} key={pack.set_name}>
            <div className="border rounded-lg p-4 cursor-pointer hover:shadow-lg transition-shadow">
              <img
                src={`http://localhost:8000/api/stickerpack/${pack.set_name}/preview`}
                alt={pack.title}
                className="w-full h-40 object-cover mb-2"
                onLoad={() => handleImageLoad(`http://localhost:8000/api/stickerpack/${pack.set_name}/preview`)}
                style={{ display: loadedImages.includes(`http://localhost:8000/api/stickerpack/${pack.set_name}/preview`) ? 'block' : 'none' }}
              />
              <h2 className="text-lg font-semibold">{pack.title}</h2>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
