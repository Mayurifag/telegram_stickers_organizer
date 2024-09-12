"use client";

import Link from 'next/link';
import { useParams } from 'next/navigation';
import { useState, useEffect } from 'react';
import axios from 'axios';

interface Sticker {
  file_id: string;
  emoji: string;
}

interface StickerPack {
  name: string;
  title: string;
  stickers: Sticker[];
}

export default function StickerPackDetail() {
  const params = useParams();
  const set_name = params.set_name as string;
  const [stickerPack, setStickerPack] = useState<StickerPack | null>(null);
  const [selectedStickers, setSelectedStickers] = useState<string[]>([]);

  useEffect(() => {
    const fetchStickerPack = async () => {
      if (set_name) {
        try {
          const cachedPack = localStorage.getItem(set_name);
          if (cachedPack) {
            setStickerPack(JSON.parse(cachedPack));
          } else {
            const response = await axios.get(`http://localhost:8000/api/stickerpack/${set_name}`);
            setStickerPack(response.data);
            localStorage.setItem(set_name, JSON.stringify(response.data));
          }
        } catch (error) {
          console.error('Error fetching sticker pack:', error);
        }
      }
    };
    fetchStickerPack();
  }, [set_name]);

  const toggleSticker = (file_id: string) => {
    setSelectedStickers((prev) =>
      prev.includes(file_id)
        ? prev.filter((id) => id !== file_id)
        : [...prev, file_id]
    );
  };

  const deleteSelectedStickers = async () => {
    try {
      await axios.post('http://localhost:8000/api/delete_stickers', { file_ids: selectedStickers });
      const response = await axios.get(`http://localhost:8000/api/stickerpack/${set_name}`);
      setStickerPack(response.data);
      setSelectedStickers([]);
      localStorage.setItem(set_name, JSON.stringify(response.data));
    } catch (error) {
      console.error('Error deleting stickers:', error);
    }
  };

  const cancelSelection = () => {
    setSelectedStickers([]);
  };

  if (!stickerPack) return <div>Loading...</div>;

  return (
    <div className="container mx-auto px-4">
      <div className="fixed top-0 left-0 right-0 bg-background shadow-md z-10 p-4 flex justify-between items-center" style={{ height: '60px' }}>
        <div>
          <Link href="/" className="text-blue-500 underline mb-4">Home</Link>
          <span className="font-bold"> {stickerPack.title}</span>
          <span> ({stickerPack.stickers.length} stickers)</span>
        </div>
        <div>
          {selectedStickers.length > 0 && (
            <>
              <button
                className="bg-red-500 text-white px-4 py-2 rounded mr-2"
                onClick={deleteSelectedStickers}
              >
                Delete Selected Stickers ({selectedStickers.length})
              </button>
              <button
                className="bg-gray-300 text-black px-4 py-2 rounded"
                onClick={cancelSelection}
              >
                Cancel Selection
              </button>
            </>
          )}
        </div>
      </div>
      <div className="mt-16">
        <div className="flex flex-wrap">
          {stickerPack.stickers.map((sticker) => (
            <div key={sticker.file_id} className="flex flex-col items-center w-1/2 sm:w-1/4 md:w-1/5 lg:w-1/6 xl:w-1/7">
              <div
                className={`relative cursor-pointer`}
                onClick={() => toggleSticker(sticker.file_id)}
                style={{
                  border: selectedStickers.includes(sticker.file_id) ? '3px solid red' : '3px solid transparent',
                  boxSizing: 'border-box'
                }}
              >
                <img
                  src={`http://localhost:8000/api/sticker/${sticker.file_id}`}
                  alt={sticker.emoji}
                  className="w-full h-auto max-w-[300px] object-contain p-1"
                />
              </div>
              <span className="mt-2">
                {sticker.emoji}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
