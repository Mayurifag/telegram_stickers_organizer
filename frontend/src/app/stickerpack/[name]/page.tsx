"use client";

import Link from 'next/link';
import { useParams } from 'next/navigation';
import { useState, useEffect } from 'react';
import axios from 'axios';
import { RenderSticker } from '@/app/components/RenderSticker';

interface Sticker {
  file_id: string;
  emoji: string;
  is_animated: boolean;
  is_video: boolean;
}

interface StickerPack {
  name: string;
  title: string;
  user_id: number;
  stickers: Sticker[];
}

export default function StickerPackDetail() {
  const params = useParams();
  const name = params.name as string;
  const [stickerPack, setStickerPack] = useState<StickerPack | null>(null);
  const [selectedStickers, setSelectedStickers] = useState<string[]>([]);
  const [selectedStickerForMove, setSelectedStickerForMove] = useState<string | null>(null);
  const [stickerPacksForMove, setStickerPacksForMove] = useState<StickerPack[]>([]);

  useEffect(() => {
    const fetchStickerPack = async () => {
      if (name) {
        try {
          const response = await axios.get(`http://localhost:8000/api/stickerpack/${name}`);
          setStickerPack(response.data);
        } catch (error) {
          console.error('Error fetching sticker pack:', error);
        }
      }
    };
    fetchStickerPack();
  }, [name]);

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
      const response = await axios.get(`http://localhost:8000/api/stickerpack/${name}`);
      setStickerPack(response.data);
      setSelectedStickers([]);
    } catch (error) {
      console.error('Error deleting stickers:', error);
    }
  };

  const cancelSelection = () => {
    setSelectedStickers([]);
  };

  const handleContextMenu = async (event: React.MouseEvent, sticker: Sticker) => {
    event.preventDefault();
    setSelectedStickerForMove(sticker.file_id);
    const response = await axios.get('http://localhost:8000/api/stickerpacks');
    setStickerPacksForMove(response.data.filter((pack: StickerPack) => pack.name !== stickerPack?.name));
  };

  const handleMoveSticker = async (destinationPack: StickerPack) => {
    if (selectedStickerForMove && stickerPack) {
      try {
        const response = await axios.post('http://localhost:8000/api/move_sticker', {
          source_pack: stickerPack.name,
          destination_pack: destinationPack.name,
          file_id: selectedStickerForMove,
          user_id: stickerPack.user_id
        });

        if (response.data.success) {
          // Refresh the sticker pack data after successful move
          const updatedPackResponse = await axios.get(`http://localhost:8000/api/stickerpack/${name}`);
          setStickerPack(updatedPackResponse.data);
          setSelectedStickerForMove(null);
        }
      } catch (error) {
        if (axios.isAxiosError(error) && error.response) {
          alert(`Error moving sticker: ${error.response.data.error}`);
        } else {
          alert('An unexpected error occurred while moving the sticker');
        }
        console.error(`Error moving sticker to pack: ${destinationPack.name}`, error);
      }
    }
    setSelectedStickerForMove(null);
  };

  return (
    <div className="container mx-auto px-4">
      <div className="fixed top-0 left-0 right-0 bg-background shadow-md z-10 p-4 flex justify-between items-center" style={{ height: '60px' }}>
        <div>
          <Link href="/" className="text-blue-500 underline mb-4">Home</Link>
          {stickerPack && (
            <>
              <span className="font-bold"> {stickerPack.title}</span>
              <span> ({stickerPack.stickers.length} stickers) (User ID: {stickerPack.user_id ?? 'N/A'})</span>
            </>
          )}
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
      <div className={`mt-16 ${selectedStickerForMove ? 'opacity-50' : ''}`}>
        <div className="flex flex-wrap">
          {stickerPack?.stickers.map((sticker) => (
            <div key={sticker.file_id} className="flex flex-col items-center w-1/2 sm:w-1/4 md:w-1/5 lg:w-1/6 xl:w-1/7">
              <div
                className={`relative cursor-pointer`}
                onClick={() => toggleSticker(sticker.file_id)}
                onContextMenu={(event) => handleContextMenu(event, sticker)}
                style={{
                  border: selectedStickers.includes(sticker.file_id) ? '3px solid red' : '3px solid transparent',
                  boxSizing: 'border-box'
                }}
              >
                <RenderSticker sticker={sticker} />
              </div>
              <span className="mt-2">
                {sticker.emoji}
              </span>
            </div>
          ))}
        </div>
      </div>
      {selectedStickerForMove && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
          <div className="bg-modal p-4 rounded shadow">
            <h2 className="text-xl font-bold mb-4">Move Sticker To:</h2>
            {stickerPacksForMove.map((pack) => (
              <button
                key={pack.name}
                className="block w-full bg-blue-400 text-white px-4 py-2 rounded mb-2"
                onClick={() => handleMoveSticker(pack)}
              >
                {pack.title}
              </button>
            ))}
            <button
              className="block w-full bg-gray-500 text-black mt-6 px-4 py-2 rounded"
              onClick={() => setSelectedStickerForMove(null)}
            >
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
