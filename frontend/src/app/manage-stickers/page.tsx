"use client";

import { useState, useEffect } from 'react';
import axios from 'axios';
import Link from 'next/link';

interface StickerSet {
  set_name: string;
  title: string;
  user_id: number;
}

export default function ManageStickers() {
  const [stickerSets, setStickerSets] = useState<StickerSet[]>([]);

  useEffect(() => {
    fetchStickerSets();
  }, []);

  const fetchStickerSets = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/all_sticker_sets');
      setStickerSets(response.data);
    } catch (error) {
      console.error('Error fetching sticker sets:', error);
    }
  };

  const deleteStickerSet = async (setName: string) => {
    if (confirm(`Are you sure you want to delete the sticker set "${setName}"?`)) {
      try {
        await axios.post('http://localhost:8000/api/delete_sticker_set', { set_name: setName });
        fetchStickerSets(); // Refresh the list after deletion
      } catch (error) {
        console.error('Error deleting sticker set:', error);
      }
    }
  };

  const groupStickerSetsByUser = (stickerSets: StickerSet[]) => {
    return stickerSets.reduce((acc, set) => {
      (acc[set.user_id] = acc[set.user_id] || []).push(set);
      return acc;
    }, {} as Record<number, StickerSet[]>);
  };

  return (
    <div className="container mx-auto px-4">
      <h1 className="text-3xl font-bold my-4">Manage Sticker Sets</h1>
      <Link href="/" className="text-blue-500 hover:underline mb-4 inline-block">
        Back to Home
      </Link>
      <div className="grid grid-cols-1 gap-4">
        {Object.entries(groupStickerSetsByUser(stickerSets)).map(([userId, sets]) => (
          <div key={userId}>
            <h2 className="text-xl font-bold">User_id: {userId}</h2>
            {sets.map((set) => (
              <div key={set.set_name} className="border rounded-lg p-4 flex justify-between items-center">
                <div>
                  <h3 className="text-lg font-semibold">{set.title}</h3>
                  <p className="text-sm text-gray-500">{set.set_name}</p>
                </div>
                <button
                  onClick={() => deleteStickerSet(set.set_name)}
                  className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
                >
                  Delete
                </button>
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}
