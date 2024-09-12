import { useState, useEffect } from 'react';
import axios from 'axios';
import Lottie from 'lottie-react';

interface Sticker {
  file_id: string;
  is_animated: boolean;
  is_video: boolean;
}

interface RenderStickerProps {
  sticker: Sticker;
}

export function RenderSticker({ sticker }: RenderStickerProps) {
  const [animationData, setAnimationData] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const fetchAnimationData = async () => {
      if (sticker.is_animated && !animationData && !isLoading) {
        setIsLoading(true);
        try {
          const response = await axios.get(`http://localhost:8000/api/sticker/${sticker.file_id}`);
          setAnimationData(response.data);
        } catch (error) {
          console.error('Error fetching animation data:', error);
        } finally {
          setIsLoading(false);
        }
      }
    };

    fetchAnimationData();
  }, [sticker, animationData, isLoading]);

  const stickerUrl = `http://localhost:8000/api/sticker/${sticker.file_id}`;

  if (sticker.is_animated) {
    return animationData ? (
      <Lottie
        animationData={animationData}
        loop
        autoplay
        className="w-full h-auto max-w-[300px] object-contain p-1"
      />
    ) : (
      <div>...</div>
    );
  } else if (sticker.is_video) {
    return (
      <video autoPlay loop muted playsInline className="w-full h-auto max-w-[300px] object-contain p-1">
        <source src={stickerUrl} type="video/webm" />
        Your browser does not support the video tag.
      </video>
    );
  } else {
    return <img src={stickerUrl} className="w-full h-auto max-w-[300px] object-contain p-1" />;
  }
}
