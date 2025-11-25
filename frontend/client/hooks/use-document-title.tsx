import { useEffect } from "react";

export default function useDocumentTitle(title: string) {
  useEffect(() => {
    const previous = document.title;
    document.title = title;
    return () => {
      // restore previous title on unmount
      document.title = previous;
    };
  }, [title]);
}
