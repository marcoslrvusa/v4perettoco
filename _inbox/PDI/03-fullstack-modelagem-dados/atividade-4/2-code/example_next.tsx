import dynamic from 'next/dynamic';
import Image from 'next/image';

// Code splitting: só carrega quando necessário
const ChatWidget = dynamic(() => import('./ChatWidget'), { loading: () => <p /> });

export default function Landing() {
  return (
    <main>
      <Image src="/hero.webp" alt="Hero" width={1200} height={630} priority />
      <ChatWidget />  {/* lazy loaded */}
    </main>
  );
}
