Name:           kora-icon-theme
Version:        1.6.5.12
Release:        %autorelease
Summary:        forked Icon theme but with Steam Game art and others

License:        INTERNAL
URL:            https://github.com/phantomcortex/kora 
Source0:        %{name}-%version.tar.gz

BuildArch:      noarch

BuildRequires:  coreutils
Requires:       

%description


%prep
%autosetup -n %{name}-%{version}



%build
%configure
%make_build


%install

rm -rf %{buildroot}

# Create the icons directory
mkdir -p %{buildroot}%{_datadir}/icons

# Install icon themes (adjust directory names as needed based on your repo structure)
for theme_dir in kora; do
    if [ -d "$theme_dir" ]; then
        echo "Installing theme: $theme_dir"
        cp -r "$theme_dir" %{buildroot}%{_datadir}/icons/
        
        # Ensure proper permissions
        find %{buildroot}%{_datadir}/icons/"$theme_dir" -type f -exec chmod 644 {} \;
        find %{buildroot}%{_datadir}/icons/"$theme_dir" -type d -exec chmod 755 {} \;
        
        # Verify index.theme exists
        if [ ! -f %{buildroot}%{_datadir}/icons/"$theme_dir"/index.theme ]; then
            echo "Warning: index.theme missing in $theme_dir"
        fi
    fi
done


%check


%files
%license
%doc
%{_datadir}/icons/kora*/




%postun
# Update icon cache after removal
if [ $1 -eq 0 ]; then
    for theme_dir in %{_datadir}/icons/kora*; do
        if [ -d "$theme_dir" ]; then
            /bin/touch --no-create "$theme_dir" &>/dev/null || :
            if [ -x %{_bindir}/gtk-update-icon-cache ]; then
                %{_bindir}/gtk-update-icon-cache --quiet "$theme_dir" &>/dev/null || :
            fi
        fi
    done
fi


%changelog
%autochangelog
* %(date "+%a %b %d %Y") GitHub Actions <noreply@github.com> - %{version}-1
- Automated build from Git repository

