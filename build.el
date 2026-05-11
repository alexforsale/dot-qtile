;;; build --- build the documentation for publication -*- lexical-binding: t -*-
;;; Commentary:
;;; Code:
(require 'package)
(require 'org)
(setq package-user-dir (expand-file-name "./.packages"))
(setq package-archives '(("melpa" . "https://melpa.org/packages/")
                         ("elpa" . "https://elpa.gnu.org/packages/")))
(setq org-safe-remote-resources (list "https://raw.githubusercontent.com/fniessen/org-html-themes/master/org/html-theme-readtheorg.setup" "https://fniessen.github.io/org-html-themes/org/html-theme-readtheorg.setup"))

(package-initialize)
(unless package-archive-contents
  (package-refresh-contents))

(package-install 'htmlize)
(package-install 'reformatter)
(package-install 'color-theme-modern)

(require 'htmlize)
(require 'ox-publish)
(require 'font-lock)

(load-theme 'greiner t t)
(enable-theme 'greiner)

(global-font-lock-mode t)
(setq org-html-validation-link nil
      org-html-head-include-scripts nil
      org-html-head-include-default-style nil
      org-src-fontify-natively t)

(setq org-publish-project-alist
      '(("dotfiles-x"
         :components ("pages" "static"))
        ("pages"
         :recursive t
         :base-directory "./content"
         :publishing-directory "./public"
         :publishing-function org-html-publish-to-html
         :with-author t
         :with-creator nil
         :with-toc t
         :setion-numbers nil
         :time-stamp-file nil)
        ("static"
         :recursive t
         :base-directory "./assets"
         :base-extension "css\\|js\\|png\\|jpg\\|gif\\|pdf\\|mp3\\|ogg\\|swf"
         :publishing-directory "./public/assets"
         :publishing-function org-publish-attachment)))

;; Generate site

(org-publish-all t)

(message "Build completed")

(provide 'build)
;;; build.el ends here
