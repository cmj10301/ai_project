import Footer from '@/components/footer';
import Navbar from '@/components/Navbar';
import 'bootswatch/dist/litera/bootstrap.min.css';

export const metadata = {
  title: 'My App',
  description: 'Using Litera theme with Bootstrap',
};

export default function RootLayout({ children }) {
  return (
    <html lang="ko">
      <body>
        <Navbar/>
        <main className="container mt-4">
          {children}
        </main>
        <Footer/>
      </body>
    </html>
  );
}
